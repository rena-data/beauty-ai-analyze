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


def upload_report_image(analysis_id: str, image_bytes: bytes) -> str | None:
    """리포트 이미지를 Supabase Storage에 업로드, 공개 URL 반환"""
    client = get_client()
    if not client:
        return None
    try:
        path = f"reports/{analysis_id}.png"
        client.storage.from_("report-images").upload(
            path, image_bytes,
            file_options={"content-type": "image/png", "upsert": "true"}
        )
        res = client.storage.from_("report-images").get_public_url(path)
        # analyses 테이블에 이미지 URL 저장
        client.table("analyses").update(
            {"report_image_url": res}
        ).eq("id", analysis_id).execute()
        return res
    except Exception:
        return None


def get_report_image_url(analysis_id: str) -> str | None:
    """분석 ID로 리포트 이미지 URL 조회"""
    client = get_client()
    if not client:
        return None
    try:
        resp = client.table("analyses").select("report_image_url").eq("id", analysis_id).execute()
        if resp.data and resp.data[0].get("report_image_url"):
            return resp.data[0]["report_image_url"]
    except Exception:
        pass
    return None


def cleanup_old_report_images(days: int = 30) -> int:
    """N일 이상 지난 리포트 이미지를 Storage에서 삭제하고 URL을 null로 초기화"""
    client = get_client()
    if not client:
        return 0
    try:
        from datetime import datetime, timedelta
        cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
        resp = client.table("analyses").select("id, report_image_url").lt(
            "created_at", cutoff
        ).not_.is_("report_image_url", "null").execute()

        if not resp.data:
            return 0

        deleted = 0
        for row in resp.data:
            path = f"reports/{row['id']}.png"
            try:
                client.storage.from_("report-images").remove([path])
            except Exception:
                pass
            client.table("analyses").update(
                {"report_image_url": None}
            ).eq("id", row["id"]).execute()
            deleted += 1
        return deleted
    except Exception:
        return 0


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
