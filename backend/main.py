"""Beauty AI Analyze - FastAPI Backend"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from PIL import Image
import io

# Project root
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

from analyzer.color_analyzer import analyze_image
from analyzer.fashion_matcher import match_fashion
from utils.image_utils import resize_for_analysis
from utils.supabase_client import save_analysis, get_analysis, track_product_click

app = FastAPI(title="Beauty AI Analyze API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
FRONTEND = ROOT / "frontend"
app.mount("/static", StaticFiles(directory=str(FRONTEND)), name="static")


@app.get("/")
async def index():
    return FileResponse(str(FRONTEND / "index.html"))


@app.post("/api/analyze")
async def api_analyze(file: UploadFile = File(...)):
    """이미지 업로드 → 퍼스널컬러 + 얼굴 인상 분석"""
    if file.content_type not in ("image/jpeg", "image/png", "image/webp"):
        raise HTTPException(400, "지원하지 않는 이미지 형식입니다.")

    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(400, "파일 크기가 10MB를 초과합니다.")

    image = Image.open(io.BytesIO(contents))
    resized = resize_for_analysis(image)

    try:
        result = analyze_image(resized)
        # DB에 저장 (비동기, 실패해도 결과 반환)
        analysis_id = save_analysis(result)
        if analysis_id:
            result["share_id"] = analysis_id
        return result
    except HTTPException:
        raise
    except Exception as e:
        msg = str(e)
        if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
            raise HTTPException(429, "API 일일 사용량을 초과했습니다. 잠시 후 다시 시도해주세요.")
        if "503" in msg or "UNAVAILABLE" in msg:
            raise HTTPException(503, "AI 서버가 일시적으로 과부하 상태입니다. 잠시 후 다시 시도해주세요.")
        raise HTTPException(500, f"분석 중 오류가 발생했습니다: {msg}")


@app.post("/api/fashion-match")
async def api_fashion_match(file: UploadFile = File(...), season_type: str = Form("spring_warm")):
    """옷 사진 업로드 → 퍼스널컬러 매칭 분석"""
    if file.content_type not in ("image/jpeg", "image/png", "image/webp"):
        raise HTTPException(400, "지원하지 않는 이미지 형식입니다.")

    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(400, "파일 크기가 10MB를 초과합니다.")

    image = Image.open(io.BytesIO(contents))
    resized = resize_for_analysis(image)

    try:
        result = match_fashion(resized, season_type)
        return result
    except Exception as e:
        msg = str(e)
        if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
            raise HTTPException(429, "API 일일 사용량을 초과했습니다. 잠시 후 다시 시도해주세요.")
        if "503" in msg or "UNAVAILABLE" in msg:
            raise HTTPException(503, "AI 서버가 일시적으로 과부하 상태입니다. 잠시 후 다시 시도해주세요.")
        raise HTTPException(500, f"매칭 분석 중 오류가 발생했습니다: {msg}")


@app.get("/api/share/{analysis_id}")
async def get_shared_analysis(analysis_id: str):
    """공유 URL로 분석 결과 조회"""
    result = get_analysis(analysis_id)
    if not result:
        raise HTTPException(404, "분석 결과를 찾을 수 없습니다.")
    return result


@app.post("/api/track-click")
async def api_track_click(data: dict):
    """제품 클릭 추적"""
    track_product_click(
        season_type=data.get("season_type", ""),
        gender=data.get("gender", ""),
        brand=data.get("brand", ""),
        name=data.get("name", ""),
        category=data.get("category", ""),
    )
    return {"ok": True}


@app.get("/api/products/{season_type}")
async def get_products(season_type: str, gender: str = ""):
    """시즌별 뷰티/패션 제품 추천 (gender: female, male, 빈값=유니섹스)"""
    valid = ["spring_warm", "summer_cool", "autumn_warm", "winter_cool"]
    if season_type not in valid:
        raise HTTPException(400, f"잘못된 시즌 타입: {season_type}")

    data_dir = ROOT / "data"

    # 성별별 파일 선택
    beauty_file = f"beauty_products_{gender}.json" if gender else "beauty_products.json"
    fashion_file = f"fashion_products_{gender}.json" if gender else "fashion_products.json"

    # 성별 파일 없으면 기본 파일 사용
    beauty_path = data_dir / beauty_file
    if not beauty_path.exists():
        beauty_path = data_dir / "beauty_products.json"
    fashion_path = data_dir / fashion_file
    if not fashion_path.exists():
        fashion_path = data_dir / "fashion_products.json"

    with open(beauty_path, "r", encoding="utf-8") as f:
        beauty = json.load(f)
    with open(fashion_path, "r", encoding="utf-8") as f:
        fashion = json.load(f)

    return {
        "beauty": beauty.get(season_type, {}),
        "fashion": fashion.get(season_type, {}),
    }


@app.get("/api/quiz")
async def get_quiz(count: int = 5):
    """퍼스널컬러 퀴즈 랜덤 출제"""
    import random
    data_dir = ROOT / "data"
    with open(data_dir / "quiz_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    questions = data.get("questions", [])
    count = min(count, len(questions))
    selected = random.sample(questions, count)
    # 정답 제거해서 클라이언트에 전달
    for q in selected:
        q["options"] = ["spring_warm", "summer_cool", "autumn_warm", "winter_cool"]
    return {"questions": selected}


@app.post("/api/contact")
async def api_contact(data: dict):
    """문의 접수 프록시 - Apps Script + Slack으로 전달 (시크릿 서버에서만 관리)"""
    import httpx
    sheet_url = os.getenv("CONTACT_SHEET_URL", "")
    slack_url = os.getenv("CONTACT_SLACK_URL", "")

    email = data.get("email", "")
    msg_type = data.get("type", "")
    content = data.get("content", "")
    subject = data.get("subject", "")

    try:
        async with httpx.AsyncClient() as client:
            if sheet_url:
                await client.post(sheet_url, json={"email": email, "type": msg_type or subject, "content": content, "subject": subject}, timeout=10)
            if slack_url:
                text = f"📩 *문의 접수*\n*From:* {email}\n*유형:* {msg_type or subject}\n*내용:* {content}"
                await client.post(slack_url, json={"text": text}, timeout=10)
    except Exception:
        pass

    return {"ok": True}


@app.get("/api/palettes/{season_type}")
async def get_palette(season_type: str):
    """시즌별 컬러 팔레트"""
    data_dir = ROOT / "data"
    with open(data_dir / "color_palettes.json", "r", encoding="utf-8") as f:
        palettes = json.load(f)

    palette = palettes.get(season_type)
    if not palette:
        raise HTTPException(400, f"잘못된 시즌 타입: {season_type}")
    return palette
