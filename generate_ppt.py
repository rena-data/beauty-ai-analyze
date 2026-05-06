"""Beauty AI Analyze 포트폴리오 PPT 생성"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# ─── Colors ───
BG = RGBColor(0xFA, 0xFA, 0xFA)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x2D, 0x2D, 0x2D)
GRAY = RGBColor(0x6B, 0x6B, 0x6B)
LIGHT_GRAY = RGBColor(0xE8, 0xE8, 0xE8)
PRIMARY = RGBColor(0xE8, 0xA0, 0xBF)
PRIMARY_DARK = RGBColor(0xD4, 0x78, 0x9E)
GREEN = RGBColor(0x4C, 0xAF, 0x50)
BLUE = RGBColor(0x21, 0x96, 0xF3)
RED = RGBColor(0xEF, 0x53, 0x50)
ACCENT = RGBColor(0xFF, 0x8F, 0xAB)


def set_slide_bg(slide, color=BG):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_shape(slide, left, top, width, height, fill_color=WHITE, border_color=None, radius=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    return shape


def add_text(slide, left, top, width, height, text, size=14, bold=False, color=BLACK, align=PP_ALIGN.LEFT):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = align
    return txBox


def add_bullet_text(slide, left, top, width, height, items, size=13, color=BLACK):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.space_after = Pt(4)
    return txBox


# ═══════════════════════════════════════════════════════
# Slide 1: 표지
# ═══════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, WHITE)

# 상단 그라데이션 바
bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.15))
bar.fill.solid()
bar.fill.fore_color.rgb = PRIMARY
bar.line.fill.background()

add_text(slide, Inches(1), Inches(1.5), Inches(11), Inches(0.5),
         "AI PERSONAL COLOR DIAGNOSIS", 16, color=PRIMARY_DARK, align=PP_ALIGN.CENTER)
add_text(slide, Inches(1), Inches(2.2), Inches(11), Inches(1),
         "Beauty AI Analyze", 44, bold=True, color=BLACK, align=PP_ALIGN.CENTER)
add_text(slide, Inches(1), Inches(3.3), Inches(11), Inches(0.8),
         "AI 기반 퍼스널컬러 분석 & 맞춤 뷰티/패션 추천 서비스", 20, color=GRAY, align=PP_ALIGN.CENTER)
add_text(slide, Inches(1), Inches(4.5), Inches(11), Inches(0.5),
         "https://beauty-ai-analyze.onrender.com", 14, color=BLUE, align=PP_ALIGN.CENTER)
add_text(slide, Inches(1), Inches(5.5), Inches(11), Inches(0.5),
         "2026.05 | Rena", 14, color=GRAY, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════
# Slide 2: 프로젝트 개요
# ═══════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

add_text(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.6),
         "프로젝트 개요", 28, bold=True)

add_shape(slide, Inches(0.8), Inches(1.3), Inches(5.5), Inches(5.5))
add_text(slide, Inches(1.1), Inches(1.5), Inches(5), Inches(0.4),
         "문제 정의", 18, bold=True, color=PRIMARY_DARK)
add_bullet_text(slide, Inches(1.1), Inches(2.1), Inches(5), Inches(4), [
    "퍼스널컬러 컨설팅 비용: 1회 5~15만원",
    "예약 + 방문 + 1~2시간 소요",
    "온라인에서 무료로 즉시 진단받을 수 있는 서비스 부족",
    "",
    "MZ세대 '나에게 어울리는 색' 수요 폭발",
    "올리브영/무신사에서 퍼스널컬러별 추천이 트렌드",
])

add_shape(slide, Inches(7), Inches(1.3), Inches(5.5), Inches(5.5))
add_text(slide, Inches(7.3), Inches(1.5), Inches(5), Inches(0.4),
         "해결 방안", 18, bold=True, color=GREEN)
add_bullet_text(slide, Inches(7.3), Inches(2.1), Inches(5), Inches(4), [
    "사진 한 장 → AI가 즉시 퍼스널컬러 진단",
    "전문 컨설턴트급 분석 결과 무료 제공",
    "맞춤 뷰티/패션 제품 추천 (실제 판매 제품)",
    "",
    "회원가입 없이 즉시 사용",
    "운영 비용 $0/월 (완전 무료 인프라)",
    "모바일/PC 반응형 지원",
])


# ═══════════════════════════════════════════════════════
# Slide 3: 핵심 기능
# ═══════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

add_text(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.6),
         "핵심 기능", 28, bold=True)

features = [
    ("🎨", "퍼스널컬러 분석", "4계절 시즌 타입 진단\n매칭률 차트 + S/A/B/C 등급"),
    ("👤", "얼굴 인상 분석", "피부/눈동자/머리카락 분석\n레이더 차트 5축"),
    ("🖌", "컬러 드레이핑", "얼굴+컬러 배경 비교\nBest 4 vs Worst 4"),
    ("💄", "뷰티 제품 추천", "올리브영 베스트셀러 80개\n성별별 맞춤 추천"),
    ("👗", "패션 제품 추천", "무신사 베스트셀러 37개\n실제 구매 링크 연결"),
    ("👔", "옷 매칭 분석", "옷 사진 업로드 → 궁합 분석\nS/A/B/C 등급 판정"),
    ("💅", "스타일링 가이드", "메이크업 포인트 카드\n컬러 팔레트 3행"),
    ("📤", "결과 공유", "리포트 다운로드\nX/Facebook/URL 공유"),
]

for i, (emoji, title, desc) in enumerate(features):
    col = i % 4
    row = i // 4
    x = Inches(0.8 + col * 3.1)
    y = Inches(1.3 + row * 3)

    add_shape(slide, x, y, Inches(2.8), Inches(2.6))
    add_text(slide, x, y + Inches(0.2), Inches(2.8), Inches(0.5),
             emoji, 32, align=PP_ALIGN.CENTER)
    add_text(slide, x, y + Inches(0.8), Inches(2.8), Inches(0.4),
             title, 16, bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, x, y + Inches(1.3), Inches(2.8), Inches(1),
             desc, 12, color=GRAY, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════
# Slide 4: 기술 스택
# ═══════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

add_text(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.6),
         "기술 스택 & 아키텍처", 28, bold=True)

stacks = [
    ("Frontend", "HTML5, CSS3\nVanilla JavaScript\nPretendard Font", ACCENT),
    ("Backend", "Python FastAPI\nUvicorn\nRender (Free)", GREEN),
    ("AI Engine", "Google Gemini\nVision API\n모델 폴백 체인 4개", BLUE),
    ("Database", "Supabase\n(PostgreSQL)\n분석 통계 + 공유 URL", RGBColor(0x3E, 0xCF, 0x8E)),
]

for i, (label, desc, color) in enumerate(stacks):
    x = Inches(0.8 + i * 3.1)
    shape = add_shape(slide, x, Inches(1.3), Inches(2.8), Inches(2.5))
    shape.fill.fore_color.rgb = color
    add_text(slide, x, Inches(1.5), Inches(2.8), Inches(0.4),
             label, 18, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(slide, x, Inches(2.1), Inches(2.8), Inches(1.2),
             desc, 13, color=WHITE, align=PP_ALIGN.CENTER)

# 보조 서비스
add_text(slide, Inches(0.8), Inches(4.2), Inches(11), Inches(0.4),
         "보조 서비스", 16, bold=True, color=GRAY)

aux = [
    ("Google Analytics 4", "유저 행동 분석"),
    ("UptimeRobot", "서버 슬립 방지 (5분 핑)"),
    ("Google Sheets", "문의 자동 기록 + 이메일 알림"),
    ("Google Search Console", "SEO + 검색 노출"),
]
for i, (name, desc) in enumerate(aux):
    x = Inches(0.8 + i * 3.1)
    add_shape(slide, x, Inches(4.8), Inches(2.8), Inches(1.2))
    add_text(slide, x, Inches(4.9), Inches(2.8), Inches(0.4),
             name, 13, bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, x, Inches(5.3), Inches(2.8), Inches(0.4),
             desc, 11, color=GRAY, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════
# Slide 5: AI 엔진 상세
# ═══════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

add_text(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.6),
         "AI 엔진 - 모델 폴백 체인 & 키 이중화", 28, bold=True)

add_shape(slide, Inches(0.8), Inches(1.3), Inches(7), Inches(5.5))
add_text(slide, Inches(1.1), Inches(1.5), Inches(6.5), Inches(0.4),
         "모델 폴백 체인", 18, bold=True, color=BLUE)
add_bullet_text(slide, Inches(1.1), Inches(2.1), Inches(6.5), Inches(4), [
    "1순위: gemini-2.5-flash (최고 성능)",
    "  ↓ 503/429 에러 시",
    "2순위: gemini-2.5-flash-lite",
    "  ↓ 실패 시",
    "3순위: gemini-2.0-flash",
    "  ↓ 실패 시",
    "4순위: gemini-3-flash-preview",
    "",
    "각 모델당 2회 재시도 + 키 자동 전환",
    "최대 16번 시도 후에야 에러 반환",
    "",
    "temperature=0.0 → 동일 사진 동일 결과 보장",
])

add_shape(slide, Inches(8.2), Inches(1.3), Inches(4.3), Inches(5.5))
add_text(slide, Inches(8.5), Inches(1.5), Inches(3.8), Inches(0.4),
         "핵심 수치", 18, bold=True, color=GREEN)
add_bullet_text(slide, Inches(8.5), Inches(2.1), Inches(3.8), Inches(4), [
    "일일 분석 가능: 3,000회",
    "  (API 키 2개 × 1,500회)",
    "",
    "분석 소요 시간: 10~15초",
    "",
    "API 비용: $0/월",
    "  (Gemini 무료 티어)",
    "",
    "확신도 차등 적용:",
    "  자연광: 80~92%",
    "  실내: 65~80%",
    "  불량: 45~65%",
])


# ═══════════════════════════════════════════════════════
# Slide 6: 제품 추천 시스템
# ═══════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

add_text(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.6),
         "제품 추천 시스템", 28, bold=True)

add_shape(slide, Inches(0.8), Inches(1.3), Inches(5.5), Inches(5.5))
add_text(slide, Inches(1.1), Inches(1.5), Inches(5), Inches(0.4),
         "뷰티 (올리브영 기반)", 18, bold=True, color=PRIMARY_DARK)
add_bullet_text(slide, Inches(1.1), Inches(2.1), Inches(5), Inches(4), [
    "총 80개 제품 (시즌별 20개)",
    "",
    "립: 롬앤, 페리페라, 퓌, 힌스",
    "아이: 웨이크메이크(3년1위), 클리오",
    "치크: 롬앤, 크리니크, 페리페라(화해1위)",
    "베이스: 정샘물(3년1위), VDL(1등파데)",
    "",
    "올리브영 2025 어워즈 수상작 기반",
    "실제 제품 페이지 직접 연결",
])

add_shape(slide, Inches(7), Inches(1.3), Inches(5.5), Inches(5.5))
add_text(slide, Inches(7.3), Inches(1.5), Inches(5), Inches(0.4),
         "패션 (무신사 기반)", 18, bold=True, color=BLUE)
add_bullet_text(slide, Inches(7.3), Inches(2.1), Inches(5), Inches(4), [
    "총 37개 제품 (시즌별)",
    "",
    "무신사 스탠다드 (실제 가격)",
    "커버낫 (반팔 1위)",
    "디스이즈네버댓",
    "",
    "성별별 분리 추천:",
    "  여성 / 남성 / 유니섹스",
    "",
    "무신사 제품 페이지 직접 연결",
    "구매 클릭 → Supabase 추적",
])


# ═══════════════════════════════════════════════════════
# Slide 7: 비용 구조
# ═══════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

add_text(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.6),
         "비용 구조 - 월 $0 운영", 28, bold=True)

costs = [
    ("Gemini API", "무료 (3,000회/일)", "$0"),
    ("Render 호스팅", "무료 (Free Tier)", "$0"),
    ("Supabase DB", "무료 (Free Tier)", "$0"),
    ("UptimeRobot", "무료 (50 모니터)", "$0"),
    ("Google Analytics 4", "무료", "$0"),
    ("Google Sheets", "무료 (문의 시스템)", "$0"),
    ("Google Search Console", "무료 (SEO)", "$0"),
]

add_shape(slide, Inches(2), Inches(1.3), Inches(9), Inches(0.6), fill_color=PRIMARY)
add_text(slide, Inches(2.3), Inches(1.35), Inches(4), Inches(0.5),
         "항목", 14, bold=True, color=WHITE)
add_text(slide, Inches(6), Inches(1.35), Inches(3), Inches(0.5),
         "플랜", 14, bold=True, color=WHITE)
add_text(slide, Inches(9.5), Inches(1.35), Inches(1.5), Inches(0.5),
         "월 비용", 14, bold=True, color=WHITE, align=PP_ALIGN.RIGHT)

for i, (item, plan, cost) in enumerate(costs):
    y = Inches(2.0 + i * 0.55)
    bg = WHITE if i % 2 == 0 else BG
    add_shape(slide, Inches(2), y, Inches(9), Inches(0.5), fill_color=bg)
    add_text(slide, Inches(2.3), y + Inches(0.05), Inches(4), Inches(0.4),
             item, 13)
    add_text(slide, Inches(6), y + Inches(0.05), Inches(3), Inches(0.4),
             plan, 13, color=GRAY)
    add_text(slide, Inches(9.5), y + Inches(0.05), Inches(1.5), Inches(0.4),
             cost, 13, bold=True, color=GREEN, align=PP_ALIGN.RIGHT)

# 합계
y_total = Inches(2.0 + len(costs) * 0.55 + 0.2)
add_shape(slide, Inches(2), y_total, Inches(9), Inches(0.7), fill_color=RGBColor(0xF0, 0xFF, 0xF0))
add_text(slide, Inches(2.3), y_total + Inches(0.1), Inches(4), Inches(0.5),
         "총 운영 비용", 16, bold=True)
add_text(slide, Inches(9), y_total + Inches(0.1), Inches(2), Inches(0.5),
         "$0 / 월", 20, bold=True, color=GREEN, align=PP_ALIGN.RIGHT)


# ═══════════════════════════════════════════════════════
# Slide 8: 데이터 수집 & 분석
# ═══════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

add_text(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.6),
         "데이터 수집 & 분석", 28, bold=True)

add_shape(slide, Inches(0.8), Inches(1.3), Inches(3.6), Inches(5.5))
add_text(slide, Inches(1.1), Inches(1.5), Inches(3), Inches(0.4),
         "GA4 이벤트 추적", 16, bold=True, color=BLUE)
add_bullet_text(slide, Inches(1.1), Inches(2.1), Inches(3), Inches(3.5), [
    "page_view (자동)",
    "analysis_complete",
    "product_click",
    "report_download",
    "fashion_match",
    "share (SNS별)",
    "quiz_complete",
    "",
    "쿠키 동의 시에만 활성화",
], size=12)

add_shape(slide, Inches(4.8), Inches(1.3), Inches(3.6), Inches(5.5))
add_text(slide, Inches(5.1), Inches(1.5), Inches(3), Inches(0.4),
         "Supabase 저장", 16, bold=True, color=RGBColor(0x3E, 0xCF, 0x8E))
add_bullet_text(slide, Inches(5.1), Inches(2.1), Inches(3), Inches(3.5), [
    "analyses 테이블",
    "  시즌 타입, 확신도",
    "  얼굴 분석, 스타일링",
    "  공유 URL (UUID)",
    "",
    "product_clicks 테이블",
    "  브랜드, 제품명",
    "  시즌 타입, 성별",
    "",
    "daily_stats 뷰",
    "popular_products 뷰",
], size=12)

add_shape(slide, Inches(8.8), Inches(1.3), Inches(3.6), Inches(5.5))
add_text(slide, Inches(9.1), Inches(1.5), Inches(3), Inches(0.4),
         "개인정보 보호", 16, bold=True, color=RED)
add_bullet_text(slide, Inches(9.1), Inches(2.1), Inches(3), Inches(3.5), [
    "사진: 분석 후 즉시 삭제",
    "  서버에 저장하지 않음",
    "",
    "프로필: 세션 종료 시 삭제",
    "",
    "쿠키 동의 팝업",
    "개인정보처리방침 모달",
    "",
    "Google Search Console",
    "SEO 메타태그 적용",
], size=12)


# ═══════════════════════════════════════════════════════
# Slide 9: 향후 계획
# ═══════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

add_text(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.6),
         "향후 계획", 28, bold=True)

phases = [
    ("현재", "MVP 완성", PRIMARY, [
        "퍼스널컬러 분석 + 제품 추천",
        "패션 매칭 + 퀴즈 게임",
        "SNS 공유 + 리포트 다운로드",
        "Supabase + GA4 데이터 수집",
    ]),
    ("단기", "트래픽 & 수익화", GREEN, [
        "블로그 3종 발행 (SEO)",
        "제휴 링크 (쿠팡파트너스)",
        "모바일 최적화 강화",
        "Figma 디자인 시스템",
    ]),
    ("중기", "포털 확장", BLUE, [
        "ai-test-hub 포털 메인",
        "AI 관상/얼굴상 테스트",
        "MBTI 궁합 테스트",
        "연예인 닮은꼴 테스트",
    ]),
    ("장기", "플랫폼 진화", RGBColor(0x9C, 0x27, 0xB0), [
        "심리 테스트 시리즈",
        "AR 컬러 시뮬레이션",
        "모바일 앱 검토",
        "B2B 위젯 제공",
    ]),
]

for i, (phase, title, color, items) in enumerate(phases):
    x = Inches(0.8 + i * 3.1)
    shape = add_shape(slide, x, Inches(1.3), Inches(2.8), Inches(0.7), fill_color=color)
    add_text(slide, x, Inches(1.35), Inches(2.8), Inches(0.3),
             phase, 12, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(slide, x, Inches(1.65), Inches(2.8), Inches(0.3),
             title, 14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    add_shape(slide, x, Inches(2.2), Inches(2.8), Inches(4.2))
    add_bullet_text(slide, x + Inches(0.3), Inches(2.5), Inches(2.3), Inches(3.5), items, size=12)

    # 화살표 (마지막 제외)
    if i < len(phases) - 1:
        add_text(slide, x + Inches(2.8), Inches(1.5), Inches(0.3), Inches(0.4),
                 "→", 20, bold=True, color=GRAY, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════
# Slide 10: 마무리
# ═══════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, WHITE)

bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(7.35), prs.slide_width, Inches(0.15))
bar.fill.solid()
bar.fill.fore_color.rgb = PRIMARY
bar.line.fill.background()

add_text(slide, Inches(1), Inches(1.5), Inches(11), Inches(0.8),
         "Beauty AI Analyze", 40, bold=True, color=BLACK, align=PP_ALIGN.CENTER)
add_text(slide, Inches(1), Inches(2.5), Inches(11), Inches(0.6),
         "사진 한 장으로 찾는 나만의 퍼스널컬러", 20, color=GRAY, align=PP_ALIGN.CENTER)

add_text(slide, Inches(1), Inches(3.8), Inches(11), Inches(0.5),
         "Live   https://beauty-ai-analyze.onrender.com", 14, color=BLUE, align=PP_ALIGN.CENTER)
add_text(slide, Inches(1), Inches(4.3), Inches(11), Inches(0.5),
         "GitHub   https://github.com/rena-data/beauty-ai-analyze", 14, color=BLUE, align=PP_ALIGN.CENTER)

add_text(slide, Inches(1), Inches(5.5), Inches(11), Inches(0.5),
         "감사합니다", 24, bold=True, color=BLACK, align=PP_ALIGN.CENTER)

add_text(slide, Inches(1), Inches(6.3), Inches(11), Inches(0.5),
         "Rena | contact@beautyai-analyze.com", 14, color=GRAY, align=PP_ALIGN.CENTER)


# ─── 저장 ───
output = "/Users/data_team/Desktop/rena_zip/project/beauty_ai_analyze/Beauty_AI_Analyze_Portfolio.pptx"
prs.save(output)
print(f"PPT 생성 완료: {output}")
