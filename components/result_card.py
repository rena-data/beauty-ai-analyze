"""분석 결과 카드 컴포넌트"""

import streamlit as st

from analyzer.color_types import SEASON_TYPES


def render_result_header(analysis: dict):
    """시즌 타입 + 확신도 헤더"""
    season = SEASON_TYPES.get(analysis["season_type"])
    if not season:
        return

    confidence = analysis.get("confidence", 0)
    conf_pct = int(confidence * 100)
    conf_class = (
        "confidence-high" if confidence >= 0.75
        else "confidence-medium" if confidence >= 0.5
        else "confidence-low"
    )
    season_class = analysis["season_type"].split("_")[0]
    season_detail = analysis.get("season_detail", season.name_ko)
    one_line = analysis.get("one_line_conclusion", "")

    st.markdown(f"""
    <div class="result-card">
        <div class="result-header">
            <div>
                <span class="season-badge season-{season_class}">
                    {season.emoji} {season_detail}
                </span>
                <span style="font-size: 0.85rem; color: #6B6B6B; margin-left: 0.5rem;">
                    {season.name_en}
                </span>
            </div>
        </div>
        <div style="margin-bottom: 0.5rem;">
            <span style="font-size: 0.85rem; font-weight: 600;">분석 확신도</span>
            <span style="font-size: 0.85rem; color: #6B6B6B; float: right;">{conf_pct}%</span>
        </div>
        <div class="confidence-bar">
            <div class="confidence-fill {conf_class}" style="width: {conf_pct}%;"></div>
        </div>
        {"<div class='analysis-text' style='margin-top: 1rem; border-left-color: " + season.accent_color + ";'><strong>한 줄 결론</strong><br>" + one_line + "</div>" if one_line else ""}
    </div>
    """, unsafe_allow_html=True)


def render_face_analysis(analysis: dict):
    """얼굴 인상 분석 결과"""
    face = analysis.get("face_analysis", {})
    if not face:
        return

    skin = face.get("skin", "")
    eyes = face.get("eyes", "")
    hair = face.get("hair", "")
    face_contrast = face.get("face_contrast", "")
    strengths = face.get("strengths", [])
    improvements = face.get("improvements", [])

    strengths_html = "".join(f'<li style="margin-bottom: 0.3rem;">{s}</li>' for s in strengths)
    improvements_html = "".join(f'<li style="margin-bottom: 0.3rem;">{s}</li>' for s in improvements)

    st.markdown(f"""
    <div class="result-card">
        <div class="section-title">얼굴 인상 분석</div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem;">
            <div class="analysis-text" style="border-left-color: #FFB6C1;">
                <strong>피부</strong><br>{skin}
            </div>
            <div class="analysis-text" style="border-left-color: #87CEEB;">
                <strong>눈동자</strong><br>{eyes}
            </div>
            <div class="analysis-text" style="border-left-color: #DEB887;">
                <strong>머리카락</strong><br>{hair}
            </div>
            <div class="analysis-text" style="border-left-color: #C0C0C0;">
                <strong>대비감</strong><br>{face_contrast}
            </div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div style="background: #F0FFF0; border-radius: 12px; padding: 1rem;">
                <p style="font-weight: 700; color: #4CAF50; margin-bottom: 0.5rem;">나의 강점</p>
                <ul style="font-size: 0.9rem; color: #2D2D2D; line-height: 1.8; padding-left: 1.2rem; margin: 0;">
                    {strengths_html}
                </ul>
            </div>
            <div style="background: #FFF8F0; border-radius: 12px; padding: 1rem;">
                <p style="font-weight: 700; color: #FF9800; margin-bottom: 0.5rem;">보완 포인트</p>
                <ul style="font-size: 0.9rem; color: #2D2D2D; line-height: 1.8; padding-left: 1.2rem; margin: 0;">
                    {improvements_html}
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_draping_simulation(analysis: dict):
    """컬러 드레이핑 시뮬레이션"""
    draping = analysis.get("draping_simulation", {})
    if not draping:
        return

    good = draping.get("good_colors", [])
    bad = draping.get("bad_colors", [])

    good_html = ""
    for c in good:
        good_html += f"""
        <div style="display: flex; align-items: flex-start; gap: 0.8rem; margin-bottom: 0.8rem;">
            <div style="min-width: 40px; width: 40px; height: 40px; border-radius: 10px; background: {c.get('hex', '#CCC')}; border: 1px solid #E8E8E8; flex-shrink: 0;"></div>
            <div>
                <span style="font-weight: 700; font-size: 0.85rem;">{c.get('color', '')}</span>
                <p style="font-size: 0.82rem; color: #6B6B6B; margin: 0.2rem 0 0; line-height: 1.5;">{c.get('effect', '')}</p>
            </div>
        </div>"""

    bad_html = ""
    for c in bad:
        bad_html += f"""
        <div style="display: flex; align-items: flex-start; gap: 0.8rem; margin-bottom: 0.8rem;">
            <div style="min-width: 40px; width: 40px; height: 40px; border-radius: 10px; background: {c.get('hex', '#CCC')}; border: 1px solid #E8E8E8; flex-shrink: 0;"></div>
            <div>
                <span style="font-weight: 700; font-size: 0.85rem;">{c.get('color', '')}</span>
                <p style="font-size: 0.82rem; color: #6B6B6B; margin: 0.2rem 0 0; line-height: 1.5;">{c.get('effect', '')}</p>
            </div>
        </div>"""

    st.markdown(f"""
    <div class="result-card">
        <div class="section-title">컬러 드레이핑 시뮬레이션</div>
        <div class="section-subtitle">실제 드레이핑을 했을 때 얼굴에 나타나는 변화를 분석했습니다.</div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
            <div>
                <p style="font-weight: 700; color: #4CAF50; margin-bottom: 1rem; font-size: 0.95rem;">잘 어울리는 컬러</p>
                {good_html}
            </div>
            <div>
                <p style="font-weight: 700; color: #EF5350; margin-bottom: 1rem; font-size: 0.95rem;">안 어울리는 컬러</p>
                {bad_html}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_analysis_detail(analysis: dict):
    """상세 분석 결과"""
    season = SEASON_TYPES.get(analysis["season_type"])
    if not season:
        return

    undertone = analysis.get("undertone", season.undertone)
    undertone_reason = analysis.get("undertone_reason", "")
    contrast = analysis.get("contrast_level", "중간")
    skin_desc = analysis.get("skin_description", "")
    reasoning = analysis.get("analysis_reasoning", "")
    celebrity = analysis.get("celebrity_reference", "")
    notes = analysis.get("special_notes", "")

    celebrity_html = f'<div class="analysis-text" style="margin-bottom: 1rem; border-left-color: #FFD700;"><strong>비슷한 퍼스널컬러의 연예인</strong><br>{celebrity}</div>' if celebrity else ""
    notes_html = f'<div class="analysis-text" style="border-left-color: #C0C0C0;"><strong>참고사항</strong><br>{notes}</div>' if notes else ""

    st.markdown(f"""
    <div class="result-card">
        <div class="section-title">퍼스널컬러 상세 분석</div>

        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem;">
            <div class="metric-card">
                <div class="metric-label">언더톤</div>
                <div class="metric-value" style="font-size: 1.1rem;">{undertone.split('(')[0].strip() if '(' in undertone else undertone}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">대비감</div>
                <div class="metric-value" style="font-size: 1.1rem;">{contrast}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">시즌 타입</div>
                <div class="metric-value" style="font-size: 1.1rem;">{season.emoji} {analysis.get('season_detail', season.name_ko)}</div>
            </div>
        </div>

        {"<div class='analysis-text' style='margin-bottom: 1rem; border-left-color: #E8A0BF;'><strong>언더톤 판정 근거</strong><br>" + undertone_reason + "</div>" if undertone_reason else ""}

        <div class="analysis-text" style="margin-bottom: 1rem;">
            <strong>피부톤 특성</strong><br>{skin_desc}
        </div>

        <div class="analysis-text" style="margin-bottom: 1rem;">
            <strong>분석 근거</strong><br>{reasoning}
        </div>

        {celebrity_html}
        {notes_html}
    </div>
    """, unsafe_allow_html=True)


def render_styling_tips(analysis: dict):
    """스타일링 제안"""
    styling = analysis.get("styling", {})
    if not styling:
        return

    lip = styling.get("makeup_lip", "")
    blush = styling.get("makeup_blush", "")
    eyeshadow = styling.get("makeup_eyeshadow", "")
    hair_rec = styling.get("hair_recommended", "")
    hair_avoid = styling.get("hair_avoid", "")
    fashion = styling.get("fashion_combinations", "")

    season = SEASON_TYPES.get(analysis.get("season_type", ""))
    accent = season.accent_color if season else "#E8A0BF"

    st.markdown(f"""
    <div class="result-card">
        <div class="section-title">스타일링 제안</div>

        <p style="font-weight: 700; margin: 0 0 0.8rem; font-size: 0.95rem;">메이크업</p>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.8rem; margin-bottom: 1.5rem;">
            <div class="analysis-text" style="border-left-color: #E8A0BF;">
                <strong>립</strong><br>{lip}
            </div>
            <div class="analysis-text" style="border-left-color: #FFB6C1;">
                <strong>블러셔</strong><br>{blush}
            </div>
            <div class="analysis-text" style="border-left-color: #DDA0DD;">
                <strong>아이섀도</strong><br>{eyeshadow}
            </div>
        </div>

        <p style="font-weight: 700; margin: 0 0 0.8rem; font-size: 0.95rem;">헤어컬러</p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.8rem; margin-bottom: 1.5rem;">
            <div style="background: #F0FFF0; border-radius: 12px; padding: 1rem;">
                <p style="font-weight: 600; color: #4CAF50; margin-bottom: 0.3rem; font-size: 0.85rem;">추천</p>
                <p style="font-size: 0.85rem; margin: 0; line-height: 1.6;">{hair_rec}</p>
            </div>
            <div style="background: #FFF0F0; border-radius: 12px; padding: 1rem;">
                <p style="font-weight: 600; color: #EF5350; margin-bottom: 0.3rem; font-size: 0.85rem;">피하기</p>
                <p style="font-size: 0.85rem; margin: 0; line-height: 1.6;">{hair_avoid}</p>
            </div>
        </div>

        <p style="font-weight: 700; margin: 0 0 0.8rem; font-size: 0.95rem;">패션 색 조합</p>
        <div class="analysis-text" style="border-left-color: {accent};">
            {fashion}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_season_detail(season_type_key: str):
    """시즌 타입 상세 정보"""
    season = SEASON_TYPES.get(season_type_key)
    if not season:
        return

    traits_html = "".join(f"<li>{t}</li>" for t in season.skin_traits)
    tips_html = "".join(
        f'<div class="analysis-text" style="margin-bottom: 0.5rem; border-left-color: {season.accent_color};"><strong>{cat}</strong>: {tip}</div>'
        for cat, tip in season.makeup_tips.items()
    )

    st.markdown(f"""
    <div class="result-card">
        <div class="section-title">{season.emoji} {season.name_ko} 타입 특성</div>
        <div class="analysis-text" style="margin-bottom: 1rem;">
            {season.description}
        </div>

        <p style="font-weight: 700; margin: 1rem 0 0.5rem;">피부톤 특성</p>
        <ul style="font-size: 0.9rem; color: #6B6B6B; line-height: 2;">
            {traits_html}
        </ul>

        <p style="font-weight: 700; margin: 1rem 0 0.5rem;">메이크업 팁</p>
        {tips_html}
    </div>
    """, unsafe_allow_html=True)


def render_recommendations_text(analysis: dict):
    """추천/비추천 컬러 (이유 포함)"""
    best = analysis.get("best_colors", [])
    worst = analysis.get("worst_colors", [])

    # 새 형식 (리스트 of dict) / 폴백 (텍스트)
    if best and isinstance(best[0], dict):
        best_html = ""
        for c in best:
            best_html += f"""
            <div style="display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.6rem;">
                <div style="min-width: 32px; width: 32px; height: 32px; border-radius: 8px; background: {c.get('hex', '#CCC')}; border: 1px solid #E8E8E8; flex-shrink: 0;"></div>
                <div>
                    <span style="font-weight: 700; font-size: 0.85rem;">{c.get('color', '')}</span>
                    <span style="font-size: 0.8rem; color: #6B6B6B; margin-left: 0.5rem;">{c.get('reason', '')}</span>
                </div>
            </div>"""

        worst_html = ""
        for c in worst:
            worst_html += f"""
            <div style="display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.6rem;">
                <div style="min-width: 32px; width: 32px; height: 32px; border-radius: 8px; background: {c.get('hex', '#CCC')}; border: 1px solid #E8E8E8; flex-shrink: 0;"></div>
                <div>
                    <span style="font-weight: 700; font-size: 0.85rem;">{c.get('color', '')}</span>
                    <span style="font-size: 0.8rem; color: #6B6B6B; margin-left: 0.5rem;">{c.get('reason', '')}</span>
                </div>
            </div>"""

        st.markdown(f"""
        <div class="result-card">
            <div class="section-title">추천 & 비추천 컬러</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                <div>
                    <p style="font-weight: 700; color: #4CAF50; margin-bottom: 0.8rem;">BEST 컬러</p>
                    {best_html}
                </div>
                <div>
                    <p style="font-weight: 700; color: #EF5350; margin-bottom: 0.8rem;">WORST 컬러</p>
                    {worst_html}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # 레거시 텍스트 형식 폴백
        best_exp = analysis.get("best_colors_explanation", "")
        worst_exp = analysis.get("worst_colors_explanation", "")
        st.markdown(f"""
        <div class="result-card">
            <div class="section-title">AI 맞춤 추천</div>
            <div class="analysis-text" style="margin-bottom: 1rem; border-left-color: #4CAF50;">
                <strong>어울리는 컬러</strong><br>{best_exp}
            </div>
            <div class="analysis-text" style="border-left-color: #EF5350;">
                <strong>피해야 할 컬러</strong><br>{worst_exp}
            </div>
        </div>
        """, unsafe_allow_html=True)
