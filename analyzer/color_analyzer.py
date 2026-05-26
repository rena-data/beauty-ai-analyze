"""Google Gemini Vision API를 통한 퍼스널컬러 분석 - 모델 폴백 체인"""

import io
import json
import os
import re
import time

from google import genai
from google.genai import types
from PIL import Image

from .prompts import ANALYSIS_PROMPT, ANALYSIS_SYSTEM_PROMPT

# 모델 폴백 체인: 1순위부터 시도, 실패 시 다음 모델로
MODEL_CHAIN = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-3-flash-preview",
]

MAX_RETRIES = 2
RETRY_DELAY = 3

_current_key_index = 0


def _get_api_keys():
    keys = []
    main = os.getenv("GOOGLE_API_KEY")
    backup = os.getenv("GOOGLE_API_KEY_BACKUP")
    if main:
        keys.append(main)
    if backup:
        keys.append(backup)
    if not keys:
        raise ValueError("GOOGLE_API_KEY 환경변수가 설정되지 않았습니다.")
    return keys


def _get_client():
    global _current_key_index
    keys = _get_api_keys()
    _current_key_index = _current_key_index % len(keys)
    return genai.Client(api_key=keys[_current_key_index])


def _switch_key():
    global _current_key_index
    keys = _get_api_keys()
    if len(keys) > 1:
        _current_key_index = (_current_key_index + 1) % len(keys)


def _image_to_part(image: Image.Image) -> types.Part:
    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    return types.Part.from_bytes(data=buf.getvalue(), mime_type="image/jpeg")


def _parse_json_response(text: str) -> dict:
    text = text.strip()
    # 마크다운 코드펜스 제거
    if text.startswith("```"):
        lines = text.split("\n")
        # 끝에 ```가 있으면 제거, 없으면 마지막 줄 유지
        end = -1 if lines[-1].strip().startswith("```") else len(lines)
        text = "\n".join(lines[1:end])

    # 1차: 직접 파싱 시도
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 2차: JSON 객체 부분만 추출 (앞뒤 텍스트 제거)
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start:end + 1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    # 3차: 흔한 LLM JSON 오류 정리 후 재시도
    if start != -1 and end != -1:
        cleaned = text[start:end + 1]
        # 한 줄 주석 제거 (// ...)
        cleaned = re.sub(r'//[^\n]*', '', cleaned)
        # 닫는 괄호/대괄호 앞 trailing comma 제거
        cleaned = re.sub(r',\s*([}\]])', r'\1', cleaned)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

    # 모두 실패 시 원본으로 에러 발생 (디버깅용)
    return json.loads(text)


def _call_api(model: str, img_part, system: str, prompt: str) -> dict:
    """단일 모델 + 단일 키로 API 호출"""
    client = _get_client()
    response = client.models.generate_content(
        model=model,
        contents=[prompt, img_part],
        config=types.GenerateContentConfig(
            system_instruction=system,
            response_mime_type="application/json",
            temperature=0.0,
        ),
    )
    return _parse_json_response(response.text)


def analyze_image(image: Image.Image) -> dict:
    """모델 폴백 체인 + 키 이중화로 분석 수행"""
    img_part = _image_to_part(image)
    last_err = None

    for model in MODEL_CHAIN:
        for attempt in range(MAX_RETRIES):
            try:
                result = _call_api(model, img_part, ANALYSIS_SYSTEM_PROMPT, ANALYSIS_PROMPT)

                # 얼굴 없음 감지
                if result.get("no_face"):
                    raise ValueError(result.get("no_face_reason", "사진에서 얼굴을 인식하지 못했습니다."))

                # 필수 필드 검증
                for field in ["season_type", "confidence", "undertone", "skin_description", "analysis_reasoning"]:
                    if field not in result:
                        raise ValueError(f"분석 결과에 '{field}' 필드가 누락되었습니다.")

                if result["season_type"] not in ["spring_warm", "summer_cool", "autumn_warm", "winter_cool"]:
                    raise ValueError(f"잘못된 시즌 타입: {result['season_type']}")

                return result

            except json.JSONDecodeError as e:
                last_err = e
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                    continue
                break  # JSON 파싱 실패는 재시도/다음 모델로
            except ValueError:
                raise  # 얼굴 없음, 필드 누락 등은 즉시 에러
            except Exception as e:
                last_err = e
                err_str = str(e)
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    _switch_key()
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                    continue
                break  # 이 모델 포기, 다음 모델로

    raise last_err or Exception("모든 AI 모델이 응답하지 않습니다. 잠시 후 다시 시도해주세요.")
