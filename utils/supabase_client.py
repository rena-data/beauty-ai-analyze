"""Supabase 클라이언트 - 분석 통계 저장 + 제품 클릭 추적"""

import os
from supabase import create_client

_client = None


def get_client():
    global _client
    if _client is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if url and key:
            _client = create_client(url, key)
    return _client


def save_analysis(result: dict, gender: str = ""):
    """분석 결과를 DB에 저장, 생성된 ID 반환"""
    client = get_client()
    if not client:
        return None
    try:
        row = {
            "season_type": result.get("season_type"),
            "season_detail": result.get("season_detail"),
            "confidence": result.get("confidence"),
            "undertone": result.get("undertone"),
            "season_rates": result.get("season_rates"),
            "face_analysis": result.get("face_analysis"),
            "draping_simulation": result.get("draping_simulation"),
            "best_colors": result.get("best_colors"),
            "worst_colors": result.get("worst_colors"),
            "styling": result.get("styling"),
            "one_line_conclusion": result.get("one_line_conclusion"),
            "gender": gender,
        }
        resp = client.table("analyses").insert(row).execute()
        if resp.data:
            return resp.data[0]["id"]
    except Exception:
        pass
    return None


def get_analysis(analysis_id: str) -> dict | None:
    """ID로 분석 결과 조회 (공유 URL용)"""
    client = get_client()
    if not client:
        return None
    try:
        resp = client.table("analyses").select("*").eq("id", analysis_id).execute()
        if resp.data:
            return resp.data[0]
    except Exception:
        pass
    return None


def track_product_click(season_type: str, gender: str, brand: str, name: str, category: str = ""):
    """제품 클릭 추적"""
    client = get_client()
    if not client:
        return
    try:
        client.table("product_clicks").insert({
            "season_type": season_type,
            "gender": gender,
            "product_brand": brand,
            "product_name": name,
            "product_category": category,
        }).execute()
    except Exception:
        pass
