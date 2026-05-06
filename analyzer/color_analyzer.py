"""Google Gemini 2.5 Flash Vision API를 통한 퍼스널컬러 분석"""

import io
import json
import os
import time

from google import genai
from google.genai import types
from PIL import Image

from .prompts import ANALYSIS_PROMPT, ANALYSIS_SYSTEM_PROMPT, NO_FACE_PROMPT

MAX_RETRIES = 3
RETRY_DELAYS = [2, 5, 10]  # 초


def _get_client():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY 환경변수가 설정되지 않았습니다.")
    return genai.Client(api_key=api_key)


def _image_to_part(image: Image.Image) -> types.Part:
    """PIL Image를 Gemini Part로 변환"""
    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    return types.Part.from_bytes(data=buf.getvalue(), mime_type="image/jpeg")


def _parse_json_response(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1])
    return json.loads(text)


def _call_with_retry(fn):
    """503/429 에러 시 자동 재시도"""
    last_err = None
    for attempt in range(MAX_RETRIES):
        try:
            return fn()
        except Exception as e:
            err_str = str(e)
            if "503" in err_str or "UNAVAILABLE" in err_str or "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                last_err = e
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAYS[attempt])
                    continue
            raise
    raise last_err


def check_face(image: Image.Image) -> dict:
    """이미지에 얼굴이 있는지 확인"""
    client = _get_client()
    img_part = _image_to_part(image)

    def _call():
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[NO_FACE_PROMPT, img_part],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.3,
            ),
        )
        return _parse_json_response(response.text)

    return _call_with_retry(_call)


def analyze_image(image: Image.Image) -> dict:
    """이미지에서 퍼스널컬러를 분석하여 결과 반환"""
    client = _get_client()
    img_part = _image_to_part(image)

    def _call():
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[ANALYSIS_PROMPT, img_part],
            config=types.GenerateContentConfig(
                system_instruction=ANALYSIS_SYSTEM_PROMPT,
                response_mime_type="application/json",
                temperature=0.3,
            ),
        )
        return _parse_json_response(response.text)

    result = _call_with_retry(_call)

    # 필수 필드 검증
    required_fields = [
        "season_type", "confidence", "undertone", "skin_description",
        "analysis_reasoning",
    ]
    for field in required_fields:
        if field not in result:
            raise ValueError(f"분석 결과에 '{field}' 필드가 누락되었습니다.")

    valid_types = ["spring_warm", "summer_cool", "autumn_warm", "winter_cool"]
    if result["season_type"] not in valid_types:
        raise ValueError(f"잘못된 시즌 타입: {result['season_type']}")

    return result
