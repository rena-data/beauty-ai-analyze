"""제품 추천 카드 그리드 컴포넌트"""

import json
import streamlit as st


@st.cache_data
def load_beauty_products():
    with open("data/beauty_products.json", "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def load_fashion_products():
    with open("data/fashion_products.json", "r", encoding="utf-8") as f:
        return json.load(f)


def _format_price(price: int) -> str:
    return f"{price:,}원"


def _render_product_card(product: dict) -> str:
    """단일 제품 카드 HTML"""
    return f"""
    <div class="product-card">
        <div class="product-brand">{product['brand']}</div>
        <div class="product-name">{product['name']}</div>
        <div class="product-price">{_format_price(product['price'])}</div>
        <div class="product-reason">{product['reason']}</div>
    </div>
    """


def render_beauty_products(season_key: str):
    """뷰티 제품 추천 그리드"""
    products = load_beauty_products()
    season_products = products.get(season_key)
    if not season_products:
        return

    category_labels = {
        "lip": ("Lip", "립 메이크업"),
        "eye": ("Eye", "아이 메이크업"),
        "cheek": ("Cheek", "치크 & 블러셔"),
        "base": ("Base", "베이스 메이크업"),
    }

    st.markdown("""
    <div class="result-card">
        <div class="section-title">추천 뷰티 제품</div>
        <div class="section-subtitle">당신의 퍼스널컬러에 딱 맞는 제품들을 엄선했어요.</div>
    """, unsafe_allow_html=True)

    for cat_key, (cat_en, cat_ko) in category_labels.items():
        items = season_products.get(cat_key, [])
        if not items:
            continue

        # 카테고리당 최대 3개
        items = items[:3]

        st.markdown(f"""
        <p style="font-weight: 700; font-size: 0.9rem; color: #6B6B6B; margin: 1.2rem 0 0.8rem; text-transform: uppercase; letter-spacing: 0.05em;">
            {cat_en} &mdash; {cat_ko}
        </p>
        """, unsafe_allow_html=True)

        cols = st.columns(len(items))
        for i, item in enumerate(items):
            with cols[i]:
                st.markdown(_render_product_card(item), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_fashion_products(season_key: str):
    """패션 제품 추천 그리드"""
    products = load_fashion_products()
    season_products = products.get(season_key)
    if not season_products:
        return

    category_labels = {
        "top": ("Top", "상의"),
        "bottom": ("Bottom", "하의"),
        "outer": ("Outer", "아우터"),
    }

    st.markdown("""
    <div class="result-card">
        <div class="section-title">추천 패션 아이템</div>
        <div class="section-subtitle">당신의 컬러에 어울리는 패션 아이템을 추천해드려요.</div>
    """, unsafe_allow_html=True)

    for cat_key, (cat_en, cat_ko) in category_labels.items():
        items = season_products.get(cat_key, [])
        if not items:
            continue

        items = items[:3]

        st.markdown(f"""
        <p style="font-weight: 700; font-size: 0.9rem; color: #6B6B6B; margin: 1.2rem 0 0.8rem; text-transform: uppercase; letter-spacing: 0.05em;">
            {cat_en} &mdash; {cat_ko}
        </p>
        """, unsafe_allow_html=True)

        cols = st.columns(len(items))
        for i, item in enumerate(items):
            with cols[i]:
                color_hex = item.get("color_hex", "")
                color_dot = ""
                if color_hex:
                    color_dot = f'<div style="width:16px;height:16px;border-radius:50%;background:{color_hex};border:1px solid #E8E8E8;display:inline-block;vertical-align:middle;margin-right:6px;"></div>'

                st.markdown(f"""
                <div class="product-card">
                    <div class="product-brand">{item['brand']}</div>
                    <div class="product-name">{color_dot}{item['name']}</div>
                    <div class="product-price">{_format_price(item['price'])}</div>
                    <div class="product-reason">{item['reason']}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
