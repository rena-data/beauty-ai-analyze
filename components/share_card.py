"""공유용 9:16 프리미엄 리포트 이미지 생성"""

import io
import textwrap

import streamlit as st
from PIL import Image, ImageDraw, ImageFont

from analyzer.color_types import SEASON_TYPES

# ─── 이미지 크기 (9:16) ───
W, H = 1080, 1920
MARGIN = 60
COL_W = (W - MARGIN * 3) // 2


def _font(size: int) -> ImageFont.FreeTypeFont:
    """한국어 시스템 폰트 로드"""
    paths = [
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def _wrap(text: str, max_chars: int = 28) -> list[str]:
    """한국어 텍스트 줄바꿈"""
    lines = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            continue
        wrapped = textwrap.wrap(paragraph, width=max_chars)
        lines.extend(wrapped if wrapped else [""])
    return lines


def _draw_text_block(draw: ImageDraw.Draw, x: int, y: int, text: str,
                     font: ImageFont.FreeTypeFont, fill: str, max_w: int,
                     line_spacing: int = 6) -> int:
    """텍스트 블록 그리기. 사용한 높이 반환."""
    max_chars = max(10, max_w // (font.size * 2 // 3))
    lines = _wrap(text, max_chars)
    total_h = 0
    for line in lines:
        draw.text((x, y + total_h), line, fill=fill, font=font)
        total_h += font.size + line_spacing
    return total_h


def _draw_color_chip(draw: ImageDraw.Draw, x: int, y: int, hex_color: str,
                     size: int = 48, radius: int = 10):
    """컬러칩 그리기"""
    draw.rounded_rectangle([(x, y), (x + size, y + size)],
                           radius=radius, fill=hex_color, outline="#E0E0E0")


def create_share_image(analysis: dict) -> Image.Image:
    """9:16 비주얼 진단 리포트 이미지 생성"""
    season = SEASON_TYPES.get(analysis.get("season_type"))
    if not season:
        return None

    img = Image.new("RGB", (W, H), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    # Fonts
    f_title = _font(42)
    f_subtitle = _font(28)
    f_section = _font(26)
    f_body = _font(22)
    f_small = _font(18)
    f_label = _font(16)

    accent = season.accent_color
    r, g, b = int(accent[1:3], 16), int(accent[3:5], 16), int(accent[5:7], 16)
    y = 0

    # ─── Header gradient ───
    header_h = 220
    for i in range(header_h):
        ratio = i / header_h
        cr = int(r + (250 - r) * ratio)
        cg = int(g + (250 - g) * ratio)
        cb = int(b + (250 - b) * ratio)
        draw.line([(0, i), (W, i)], fill=(cr, cg, cb))

    draw.text((MARGIN, 40), "Personal Color & Face Analysis", fill="#FFFFFF", font=f_small)
    draw.text((MARGIN, 70), "퍼스널 컬러 & 얼굴 인상 분석 리포트", fill="#FFFFFF", font=f_title)

    season_detail = analysis.get("season_detail", season.name_ko)
    draw.text((MARGIN, 130), f"{season.emoji} {season_detail}", fill="#FFFFFF", font=f_subtitle)

    conf = int(analysis.get("confidence", 0) * 100)
    draw.text((W - MARGIN - 150, 130), f"확신도 {conf}%", fill="#FFFFFF", font=f_subtitle)

    # Undertone badge
    undertone = analysis.get("undertone", season.undertone)
    short_ut = undertone.split("(")[0].strip() if "(" in undertone else undertone
    draw.rounded_rectangle([(MARGIN, 175), (MARGIN + 200, 205)], radius=15, fill="#FFFFFF")
    draw.text((MARGIN + 15, 179), short_ut, fill=accent, font=f_small)

    y = header_h + 20

    # ─── 한 줄 결론 ───
    conclusion = analysis.get("one_line_conclusion", "")
    if conclusion:
        draw.rounded_rectangle([(MARGIN, y), (W - MARGIN, y + 60)],
                               radius=12, fill="#FFF8F0", outline="#FFE0C0")
        _draw_text_block(draw, MARGIN + 15, y + 12, conclusion, f_body, "#2D2D2D", W - MARGIN * 2 - 30)
        y += 80

    # ─── 드레이핑 시뮬레이션 ───
    draping = analysis.get("draping_simulation", {})
    good_colors = draping.get("good_colors", [])
    bad_colors = draping.get("bad_colors", [])

    if good_colors or bad_colors:
        draw.text((MARGIN, y), "컬러 드레이핑", fill="#2D2D2D", font=f_section)
        y += 40

        # Good colors
        draw.text((MARGIN, y), "BEST", fill="#4CAF50", font=f_section)
        y += 36
        for c in good_colors[:4]:
            hex_c = c.get("hex", "#CCCCCC")
            _draw_color_chip(draw, MARGIN, y, hex_c, 44)
            draw.text((MARGIN + 58, y + 2), c.get("color", ""), fill="#2D2D2D", font=f_body)
            effect_y = _draw_text_block(draw, MARGIN + 58, y + 28, c.get("effect", ""),
                                        f_small, "#6B6B6B", W - MARGIN * 2 - 70)
            y += max(50, 28 + effect_y) + 8
        y += 10

        # Bad colors
        draw.text((MARGIN, y), "WORST", fill="#EF5350", font=f_section)
        y += 36
        for c in bad_colors[:4]:
            hex_c = c.get("hex", "#CCCCCC")
            _draw_color_chip(draw, MARGIN, y, hex_c, 44)
            draw.text((MARGIN + 58, y + 2), c.get("color", ""), fill="#2D2D2D", font=f_body)
            effect_y = _draw_text_block(draw, MARGIN + 58, y + 28, c.get("effect", ""),
                                        f_small, "#6B6B6B", W - MARGIN * 2 - 70)
            y += max(50, 28 + effect_y) + 8
        y += 15

    # ─── Divider ───
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill="#E8E8E8", width=1)
    y += 20

    # ─── 얼굴 인상 분석 ───
    face = analysis.get("face_analysis", {})
    if face:
        draw.text((MARGIN, y), "얼굴 인상 분석", fill="#2D2D2D", font=f_section)
        y += 40

        for label, key, color in [
            ("피부", "skin", "#FFB6C1"),
            ("눈동자", "eyes", "#87CEEB"),
            ("머리카락", "hair", "#DEB887"),
        ]:
            val = face.get(key, "")
            if val:
                draw.rounded_rectangle([(MARGIN, y), (MARGIN + 8, y + 20)],
                                       radius=3, fill=color)
                draw.text((MARGIN + 16, y), label, fill="#2D2D2D", font=f_body)
                y += 30
                text_h = _draw_text_block(draw, MARGIN + 16, y, val, f_small,
                                          "#6B6B6B", W - MARGIN * 2 - 20)
                y += text_h + 10

        # 강점
        strengths = face.get("strengths", [])
        if strengths:
            draw.text((MARGIN, y), "강점", fill="#4CAF50", font=f_body)
            y += 30
            for s in strengths[:3]:
                draw.text((MARGIN + 16, y), f"- {s}", fill="#2D2D2D", font=f_small)
                y += 26
            y += 10

    # ─── Divider ───
    if y < H - 300:
        draw.line([(MARGIN, y), (W - MARGIN, y)], fill="#E8E8E8", width=1)
        y += 20

    # ─── 스타일링 제안 ───
    styling = analysis.get("styling", {})
    if styling and y < H - 200:
        draw.text((MARGIN, y), "스타일링 제안", fill="#2D2D2D", font=f_section)
        y += 40

        for label, key in [("립", "makeup_lip"), ("블러셔", "makeup_blush"),
                           ("헤어 추천", "hair_recommended")]:
            val = styling.get(key, "")
            if val and y < H - 100:
                draw.text((MARGIN, y), f"{label}:", fill="#2D2D2D", font=f_body)
                y += 28
                text_h = _draw_text_block(draw, MARGIN + 16, y, val, f_small,
                                          "#6B6B6B", W - MARGIN * 2 - 20)
                y += text_h + 8

    # ─── BEST 컬러 칩 ───
    best = analysis.get("best_colors", [])
    if best and isinstance(best[0], dict) and y < H - 120:
        y = max(y, H - 150)
        draw.text((MARGIN, y), "BEST 5", fill="#4CAF50", font=f_body)
        y += 32
        for i, c in enumerate(best[:5]):
            cx = MARGIN + i * 100
            _draw_color_chip(draw, cx, y, c.get("hex", "#CCC"), 52, 12)
            draw.text((cx, y + 58), c.get("color", "")[:6], fill="#6B6B6B", font=f_label)

    # ─── Footer ───
    draw.rectangle([(0, H - 50), (W, H)], fill="#FAFAFA")
    draw.text((MARGIN, H - 40), "Beauty AI Analyze", fill="#C0C0C0", font=f_label)
    draw.text((W - MARGIN - 200, H - 40), "ai-beauty-analyze.streamlit.app",
              fill="#C0C0C0", font=f_label)

    return img


def render_share_section(analysis: dict):
    """공유 섹션 렌더링"""
    st.markdown("""
    <div class="result-card">
        <div class="section-title">결과 공유하기</div>
        <div class="section-subtitle">
            분석 결과를 9:16 리포트 이미지로 저장하여 친구들과 공유해보세요!
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("리포트 이미지 생성", key="share_btn", use_container_width=True):
        with st.spinner("리포트 이미지를 생성하고 있습니다..."):
            share_img = create_share_image(analysis)

        if share_img:
            buf = io.BytesIO()
            share_img.save(buf, format="PNG", quality=95)
            buf.seek(0)

            st.image(share_img, use_container_width=True)
            st.download_button(
                label="이미지 다운로드",
                data=buf,
                file_name="my_personal_color_report.png",
                mime="image/png",
                key="download_share",
                use_container_width=True,
            )
