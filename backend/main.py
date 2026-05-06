"""Beauty AI Analyze - FastAPI Backend"""

import json
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from PIL import Image
import io

# Project root
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

from analyzer.color_analyzer import analyze_image, check_face
from utils.image_utils import resize_for_analysis

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
        # Step 1: face check
        face_result = check_face(resized)
        if not face_result.get("has_face", False):
            raise HTTPException(
                422,
                detail=face_result.get("reason", "사진에서 얼굴을 인식하지 못했습니다."),
            )

        # Step 2: full analysis
        result = analyze_image(resized)
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
