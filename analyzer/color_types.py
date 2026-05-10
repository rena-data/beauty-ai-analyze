"""4계절 퍼스널컬러 타입 정의"""

from dataclasses import dataclass


@dataclass
class SeasonType:
    key: str
    name_ko: str
    name_en: str
    emoji: str
    undertone: str
    description: str
    skin_traits: list[str]
    best_colors: list[str]  # hex
    worst_colors: list[str]  # hex
    best_color_names: list[str]
    worst_color_names: list[str]
    makeup_tips: dict[str, str]
    fashion_keywords: list[str]
    accent_color: str  # UI 테마용


SEASON_TYPES: dict[str, SeasonType] = {
    "spring_warm": SeasonType(
        key="spring_warm",
        name_ko="봄 웜톤",
        name_en="Spring Warm",
        emoji="🌸",
        undertone="웜톤 (Yellow Undertone)",
        description="맑고 화사한 봄날의 에너지를 가진 타입입니다. 피부에 노란 기가 살짝 돌며, 밝고 선명한 컬러가 얼굴을 환하게 밝혀줍니다.",
        skin_traits=[
            "피부에 노란 기가 은은하게 감돔",
            "밝고 투명한 피부톤",
            "혈색이 좋아 보이는 복숭아빛 볼",
            "햇볕에 노출되면 금빛으로 태닝됨",
        ],
        best_colors=[
            "#E8836B", "#F0A08A", "#F5C396", "#7CB86C",
            "#E8B44C", "#4CB8A8", "#D86050", "#E89048",
            "#F2C4A8", "#F0D8B8", "#C4A888", "#B89868",
        ],
        worst_colors=[
            "#1A1A1A", "#4A4A50", "#6E2038", "#3C1858",
            "#787880", "#1C1C40",
        ],
        best_color_names=[
            "코랄", "살몬 핑크", "피치", "웜 그린",
            "골든 옐로우", "터콰이즈", "코랄 레드", "탠저린",
            "라이트 피치", "크림 베이지", "웜 베이지", "캐멀",
        ],
        worst_color_names=[
            "블랙", "차콜", "버건디", "딥 퍼플",
            "쿨 그레이", "다크 네이비",
        ],
        makeup_tips={
            "립": "코랄 핑크, 피치 핑크, 오렌지 레드 계열이 찰떡. MLBB는 로지 베이지 추천",
            "아이섀도": "코랄, 피치, 골드, 라이트 브라운 계열로 화사하게",
            "치크": "피치, 코랄, 오렌지 계열 블러셔로 자연스러운 혈색감",
            "베이스": "옐로우 베이지 톤 파운데이션. 핑크 베이스는 피부가 칙칙해 보일 수 있음",
        },
        fashion_keywords=["화사한", "밝은", "경쾌한", "내추럴", "로맨틱"],
        accent_color="#FF8FAB",
    ),
    "summer_cool": SeasonType(
        key="summer_cool",
        name_ko="여름 쿨톤",
        name_en="Summer Cool",
        emoji="🌊",
        undertone="쿨톤 (Blue/Pink Undertone)",
        description="부드럽고 우아한 여름 안개 같은 타입입니다. 피부에 핑크빛이 감돌며, 차분하고 뮤트된 컬러가 세련된 분위기를 완성합니다.",
        skin_traits=[
            "피부에 핑크빛 또는 푸른빛이 감돔",
            "부드럽고 차분한 피부톤",
            "자외선에 민감하고 쉽게 붉어짐",
            "은 주얼리가 잘 어울림",
        ],
        best_colors=[
            "#C088A0", "#9888B0", "#7898B8", "#B098C0",
            "#B890A4", "#B85878", "#7080B8", "#8870A8",
            "#68A8A0", "#D4D0E0", "#D0A8B8", "#A0BCC8",
        ],
        worst_colors=[
            "#E86820", "#D87818", "#D4A820", "#7C4820",
            "#787820", "#D85840",
        ],
        best_color_names=[
            "로즈 핑크", "라벤더", "소프트 블루", "라일락",
            "모브 핑크", "로즈 레드", "페리윙클", "소프트 퍼플",
            "쿨 민트", "라벤더 미스트", "소프트 로즈", "파우더 블루",
        ],
        worst_color_names=[
            "오렌지", "다크 오렌지", "골드", "브라운",
            "올리브", "토마토 레드",
        ],
        makeup_tips={
            "립": "로즈 핑크, 베리, 모브 핑크 계열. 오렌지 계열은 피부가 노래 보일 수 있음",
            "아이섀도": "라벤더, 로즈, 쿨 핑크, 소프트 그레이 계열",
            "치크": "로즈 핑크, 라벤더 핑크 계열로 자연스러운 혈색",
            "베이스": "핑크 베이지 톤 파운데이션. 옐로우 베이스는 칙칙해 보일 수 있음",
        },
        fashion_keywords=["우아한", "부드러운", "세련된", "클래식", "페미닌"],
        accent_color="#C8A2C8",
    ),
    "autumn_warm": SeasonType(
        key="autumn_warm",
        name_ko="가을 웜톤",
        name_en="Autumn Warm",
        emoji="🍂",
        undertone="웜톤 (Yellow/Golden Undertone)",
        description="깊고 풍요로운 가을 단풍 같은 타입입니다. 피부에 골든 베이지 기가 돌며, 따뜻하고 깊은 컬러가 고급스러운 분위기를 만듭니다.",
        skin_traits=[
            "피부에 황금빛, 올리브빛이 감돔",
            "깊이감 있는 따뜻한 피부톤",
            "햇볕에 진한 골드빛으로 태닝됨",
            "금 주얼리가 잘 어울림",
        ],
        best_colors=[
            "#B86848", "#A85838", "#787840", "#B89830",
            "#A04030", "#287060", "#783040", "#386828",
            "#C87030", "#C8A070", "#A08868", "#886048",
        ],
        worst_colors=[
            "#E860A0", "#20A0E0", "#E030A0", "#D4D0E8",
            "#88C0E0", "#F0B8C0",
        ],
        best_color_names=[
            "테라코타", "러스트", "올리브", "다크 골드",
            "브릭 레드", "딥 틸", "버건디", "포레스트 그린",
            "번트 오렌지", "캐멀", "다크 베이지", "웜 브라운",
        ],
        worst_color_names=[
            "핫 핑크", "스카이 블루", "딥 핑크", "라벤더",
            "파우더 블루", "베이비 핑크",
        ],
        makeup_tips={
            "립": "테라코타, 브릭 레드, 브라운 레드 계열. 누드 베이지도 고급스러움",
            "아이섀도": "브라운, 골드, 카키, 테라코타 계열로 깊이감 있게",
            "치크": "피치 브라운, 테라코타, 오렌지 브라운 계열",
            "베이스": "골든 베이지, 웜 베이지 톤 파운데이션. 핑크 톤은 회색빛으로 보일 수 있음",
        },
        fashion_keywords=["고급스러운", "따뜻한", "클래식", "시크", "내추럴"],
        accent_color="#CD853F",
    ),
    "winter_cool": SeasonType(
        key="winter_cool",
        name_ko="겨울 쿨톤",
        name_en="Winter Cool",
        emoji="❄️",
        undertone="쿨톤 (Blue/Neutral Undertone)",
        description="선명하고 강렬한 겨울 눈꽃 같은 타입입니다. 높은 대비감의 외모를 가지며, 비비드하고 선명한 컬러가 강렬한 존재감을 만듭니다.",
        skin_traits=[
            "피부에 푸른빛 또는 올리브빛이 감돔",
            "피부와 머리카락의 대비가 강함",
            "맑고 선명한 피부톤 (밝거나 어두움)",
            "은 주얼리와 블랙이 매우 잘 어울림",
        ],
        best_colors=[
            "#C01828", "#1A1A1A", "#FFFFFF", "#1838A0",
            "#D02868", "#3C1878", "#007080", "#A01060",
            "#007848", "#C82860", "#181838", "#A8A8B0",
        ],
        worst_colors=[
            "#E8D8B8", "#C8A880", "#C0A888", "#F0D0B0",
            "#F0D8C0", "#F0E8E0",
        ],
        best_color_names=[
            "트루 레드", "블랙", "퓨어 화이트", "로얄 블루",
            "핫 핑크", "딥 퍼플", "딥 틸", "마젠타",
            "에메랄드", "딥 핑크", "미드나잇 네이비", "실버",
        ],
        worst_color_names=[
            "밀", "버니쉬 우드", "탄", "피치 퍼프",
            "비스크", "리넨",
        ],
        makeup_tips={
            "립": "레드, 와인, 핫 핑크, 딥 베리 계열. 선명한 컬러가 찰떡",
            "아이섀도": "블랙, 실버, 네이비, 딥 퍼플 계열로 강렬하게",
            "치크": "쿨 핑크, 로즈, 베리 계열 블러셔",
            "베이스": "쿨 베이지, 뉴트럴 베이지 파운데이션. 옐로우 톤은 부자연스러움",
        },
        fashion_keywords=["시크한", "모던한", "강렬한", "도시적인", "미니멀"],
        accent_color="#DC143C",
    ),
}


def get_season_type(key: str) -> SeasonType | None:
    return SEASON_TYPES.get(key)
