"""패션 매칭 분석 - 옷 사진 → 퍼스널컬러 궁합"""

import io
import json
import os
import time

from google import genai
from google.genai import types
from PIL import Image

MODEL_CHAIN = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-3-flash-preview",
]

FASHION_MATCH_PROMPT = """이 옷/패션 아이템 사진을 분석하여 퍼스널컬러 매칭 결과를 JSON으로 반환하세요.

사용자의 퍼스널컬러 시즌 타입: {season_type}

분석 항목:
1. 옷의 주요 색상 추출 (dominant color)
2. 이 색상이 사용자의 퍼스널컬러와 얼마나 잘 어울리는지 판단
3. 4계절별 매칭률 (어떤 시즌에 가장 잘 어울리는 옷인지)
4. 착용 시 예상 효과 (피부 밝아 보임, 칙칙해 보임 등)
5. 코디 제안

만약 이미지에 옷/패션 아이템이 없으면:
{{"no_fashion": true, "reason": "옷이나 패션 아이템을 인식하지 못했습니다."}}

출력 JSON:
{{
  "item_type": "상의/하의/아우터/원피스/악세사리 등",
  "dominant_colors": [
    {{"color": "컬러명", "hex": "#XXXXXX", "percentage": 0~100}}
  ],
  "match_grade": "S | A | B | C (S=매우잘어울림, A=잘어울림, B=보통, C=안어울림)",
  "match_score": 0~100,
  "season_match": {{
    "spring_warm": 0~100,
    "summer_cool": 0~100,
    "autumn_warm": 0~100,
    "winter_cool": 0~100
  }},
  "best_season": "이 옷이 가장 잘 어울리는 시즌 타입",
  "effect_on_user": "사용자({season_type})가 이 옷을 입었을 때 예상 효과 (2-3문장)",
  "styling_tip": "이 옷과 함께 코디하면 좋은 아이템/색상 제안 (2문장)",
  "verdict": "한 줄 매칭 결론"
}}"""

_current_key_index = 0

def _get_api_keys():
    keys = []
    main = os.getenv("GOOGLE_API_KEY")
    backup = os.getenv("GOOGLE_API_KEY_BACKUP")
    if main: keys.append(main)
    if backup: keys.append(backup)
    if not keys: raise ValueError("GOOGLE_API_KEY 환경변수가 설정되지 않았습니다.")
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
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1])
    return json.loads(text)


def match_fashion(image: Image.Image, season_type: str) -> dict:
    """옷 사진 → 퍼스널컬러 매칭 분석"""
    img_part = _image_to_part(image)
    prompt = FASHION_MATCH_PROMPT.format(season_type=season_type)
    last_err = None

    for model in MODEL_CHAIN:
        for attempt in range(2):
            try:
                client = _get_client()
                response = client.models.generate_content(
                    model=model,
                    contents=[prompt, img_part],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.0,
                    ),
                )
                result = _parse_json_response(response.text)

                if result.get("no_fashion"):
                    raise ValueError(result.get("reason", "옷을 인식하지 못했습니다."))

                return result

            except ValueError:
                raise
            except Exception as e:
                last_err = e
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    _switch_key()
                if attempt < 1:
                    time.sleep(3)
                    continue
                break

    raise last_err or Exception("AI 서버가 응답하지 않습니다.")
