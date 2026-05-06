"""히어로/랜딩 섹션 + 사용자 프로필 입력 컴포넌트"""

import streamlit as st


def render_hero():
    """메인 히어로 섹션 렌더링"""
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">AI Personal Color Analysis</div>
        <div class="hero-title">당신만의 퍼스널컬러를<br>AI가 분석해드립니다</div>
        <div class="hero-subtitle">
            사진 한 장으로 전문 컨설턴트급 퍼스널컬러 진단을 받아보세요.<br>
            맞춤 뷰티 & 패션 추천까지 무료로 제공합니다.
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_upload_guide():
    """업로드 가이드 표시"""
    st.markdown("""
    <div class="result-card">
        <div class="section-title">정확한 분석을 위한 가이드</div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div>
                <p style="font-weight: 600; color: #4CAF50; margin-bottom: 0.5rem;">Good</p>
                <ul style="font-size: 0.85rem; color: #6B6B6B; line-height: 1.8; padding-left: 1.2rem;">
                    <li>자연광 아래에서 촬영</li>
                    <li>노메이크업 또는 가벼운 메이크업</li>
                    <li>얼굴이 정면으로 잘 보이는 사진</li>
                    <li>목과 쇄골까지 보이면 더 정확</li>
                </ul>
            </div>
            <div>
                <p style="font-weight: 600; color: #EF5350; margin-bottom: 0.5rem;">Avoid</p>
                <ul style="font-size: 0.85rem; color: #6B6B6B; line-height: 1.8; padding-left: 1.2rem;">
                    <li>강한 조명 (형광등, 직사광선)</li>
                    <li>진한 메이크업 상태</li>
                    <li>필터가 적용된 사진</li>
                    <li>선글라스나 마스크 착용</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_user_profile() -> dict:
    """사용자 체형/스타일 프로필 입력"""
    st.markdown("""
    <div class="result-card">
        <div class="section-title">프로필 입력 (선택사항)</div>
        <div class="section-subtitle">입력하시면 체형과 스타일에 맞는 더 정확한 패션 추천을 받을 수 있어요.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        height = st.selectbox(
            "키",
            options=["선택 안함"] + [f"{h}cm" for h in range(145, 196)],
            index=0,
            key="user_height",
        )

    with col2:
        weight = st.selectbox(
            "몸무게",
            options=["선택 안함"] + [f"{w}kg" for w in range(35, 121)],
            index=0,
            key="user_weight",
        )

    with col3:
        body_type = st.selectbox(
            "체형",
            options=[
                "선택 안함",
                "마름",
                "슬림",
                "보통",
                "근육질",
                "통통",
                "플러스",
            ],
            index=0,
            key="user_body_type",
        )

    with col4:
        style = st.selectbox(
            "평소 스타일",
            options=[
                "선택 안함",
                "캐주얼",
                "미니멀",
                "로맨틱/페미닌",
                "스트릿",
                "클래식/포멀",
                "스포티",
                "빈티지",
                "모던 시크",
            ],
            index=0,
            key="user_style",
        )

    profile = {}
    if height != "선택 안함":
        profile["height"] = height
    if weight != "선택 안함":
        profile["weight"] = weight
    if body_type != "선택 안함":
        profile["body_type"] = body_type
    if style != "선택 안함":
        profile["style"] = style

    return profile
