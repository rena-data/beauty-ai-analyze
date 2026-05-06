"""컬러 팔레트 시각화 컴포넌트"""

import json
import streamlit as st

from analyzer.color_types import SEASON_TYPES


@st.cache_data
def load_palettes():
    with open("data/color_palettes.json", "r", encoding="utf-8") as f:
        return json.load(f)


def _render_swatches(colors: list[dict]) -> str:
    """컬러 스와치 HTML 생성"""
    html = '<div class="palette-container">'
    for c in colors:
        html += f"""
        <div style="text-align: center;">
            <div class="color-swatch" style="background-color: {c['hex']};"
                 title="{c['name']} ({c['hex']})"></div>
            <div class="color-swatch-label">{c['name']}</div>
        </div>"""
    html += "</div>"
    return html


def render_color_palette(season_key: str):
    """Best vs Worst 컬러 팔레트 시각화"""
    palettes = load_palettes()
    palette = palettes.get(season_key)
    if not palette:
        return

    season = SEASON_TYPES.get(season_key)

    st.markdown(f"""
    <div class="result-card">
        <div class="section-title">
            {season.emoji} {season.name_ko} 컬러 팔레트
        </div>

        <div style="margin-bottom: 1.5rem;">
            <p style="font-weight: 700; color: #4CAF50; margin-bottom: 0.8rem; font-size: 0.95rem;">
                Best Colors - 어울리는 컬러
            </p>
            {_render_swatches(palette['best'])}
        </div>

        <div class="custom-divider"></div>

        <div>
            <p style="font-weight: 700; color: #EF5350; margin-bottom: 0.8rem; font-size: 0.95rem;">
                Worst Colors - 피해야 할 컬러
            </p>
            {_render_swatches(palette['worst'])}
        </div>
    </div>
    """, unsafe_allow_html=True)
