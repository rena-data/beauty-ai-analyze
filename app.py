"""Beauty AI Analyze - AI 퍼스널컬러 분석 & 뷰티/패션 추천 서비스"""

import streamlit as st
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

# Page config
st.set_page_config(
    page_title="Beauty AI Analyze | AI 퍼스널컬러 분석",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# Load CSS
@st.cache_data
def load_css():
    with open("assets/theme.css", "r", encoding="utf-8") as f:
        return f.read()


st.markdown(f"<style>{load_css()}</style>", unsafe_allow_html=True)

# Imports
from analyzer.color_analyzer import analyze_image, check_face
from analyzer.color_types import SEASON_TYPES
from components.hero import render_hero, render_upload_guide, render_user_profile
from components.result_card import (
    render_analysis_detail,
    render_draping_simulation,
    render_face_analysis,
    render_recommendations_text,
    render_result_header,
    render_season_detail,
    render_styling_tips,
)
from components.color_palette import render_color_palette
from components.product_grid import render_beauty_products, render_fashion_products
from components.share_card import render_share_section
from utils.image_utils import resize_for_analysis, validate_image

# ─── Session State ───
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "analyzed_image" not in st.session_state:
    st.session_state.analyzed_image = None
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}

# ─── Hero Section ───
render_hero()

# ─── Upload Section ───
col_upload, col_preview = st.columns([1, 1])

with col_upload:
    uploaded_file = st.file_uploader(
        "사진을 업로드하세요",
        type=["jpg", "jpeg", "png", "webp"],
        help="자연광에서 촬영한 노메이크업/가벼운 메이크업 사진이 가장 정확합니다.",
        key="photo_upload",
    )

    if uploaded_file:
        is_valid, msg = validate_image(uploaded_file)
        if not is_valid:
            st.error(msg)
            st.stop()

with col_preview:
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드된 사진", use_container_width=True)
    else:
        render_upload_guide()

# ─── User Profile ───
if uploaded_file:
    user_profile = render_user_profile()
    st.session_state.user_profile = user_profile

# ─── Analysis Button ───
if uploaded_file:
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    analyze_col = st.columns([1, 2, 1])
    with analyze_col[1]:
        analyze_clicked = st.button(
            "✨ AI 퍼스널컬러 분석 시작",
            key="analyze_btn",
            use_container_width=True,
        )

    if analyze_clicked:
        image = Image.open(uploaded_file)
        resized = resize_for_analysis(image)

        with st.spinner("AI가 분석 중입니다... 피부톤, 언더톤, 얼굴 인상을 종합 분석하고 있어요."):
            try:
                # Step 1: 얼굴 감지 확인
                face_check = check_face(resized)
                if not face_check.get("has_face", False):
                    st.error(
                        f"사진에서 얼굴을 인식하지 못했습니다. "
                        f"{face_check.get('reason', '정면 얼굴이 잘 보이는 사진을 업로드해주세요.')}"
                    )
                    st.stop()

                # Step 2: 퍼스널컬러 + 얼굴 인상 분석
                result = analyze_image(resized)
                st.session_state.analysis_result = result
                st.session_state.analyzed_image = image
                st.rerun()

            except Exception as e:
                st.error(f"분석 중 오류가 발생했습니다: {str(e)}")
                st.info("다시 시도하거나, 다른 사진을 업로드해보세요.")

# ─── Results Section ───
if st.session_state.analysis_result:
    result = st.session_state.analysis_result
    season_key = result["season_type"]
    season = SEASON_TYPES.get(season_key)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Result Header (시즌 타입 + 한 줄 결론)
    render_result_header(result)

    # Tabs
    tab_draping, tab_face, tab_palette, tab_styling, tab_beauty, tab_fashion, tab_detail, tab_share = st.tabs([
        "컬러 드레이핑",
        "얼굴 분석",
        f"{season.emoji} 컬러 팔레트",
        "스타일링",
        "뷰티 추천",
        "패션 추천",
        "상세 분석",
        "공유하기",
    ])

    with tab_draping:
        render_draping_simulation(result)
        render_recommendations_text(result)

    with tab_face:
        render_face_analysis(result)

    with tab_palette:
        render_color_palette(season_key)

    with tab_styling:
        render_styling_tips(result)

    with tab_beauty:
        render_beauty_products(season_key)

    with tab_fashion:
        render_fashion_products(season_key)

    with tab_detail:
        render_analysis_detail(result)
        render_season_detail(season_key)

    with tab_share:
        render_share_section(result)

    # Reset button
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    reset_col = st.columns([1, 2, 1])
    with reset_col[1]:
        if st.button("다른 사진으로 다시 분석하기", key="reset_btn"):
            st.session_state.analysis_result = None
            st.session_state.analyzed_image = None
            st.rerun()

# ─── Footer ───
st.markdown("""
<div style="text-align: center; padding: 2rem 0 1rem; color: #C0C0C0; font-size: 0.8rem;">
    Beauty AI Analyze &copy; 2026 | AI 기반 퍼스널컬러 분석 서비스<br>
    <span style="font-size: 0.75rem;">
        분석 결과는 참고용이며, 정확한 진단은 전문 컨설턴트와 상담을 권장합니다.
    </span>
</div>
""", unsafe_allow_html=True)
