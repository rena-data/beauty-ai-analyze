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
            "#FF6B6B", "#FFA07A", "#FFD93D", "#98D8AA",
            "#FF8FAB", "#FBBF77", "#E8A0BF", "#87CEEB",
            "#F4A460", "#FFB6C1", "#FFDAB9", "#90EE90",
        ],
        worst_colors=[
            "#000000", "#2F4F4F", "#800020", "#4A0E4E",
            "#808080", "#191970",
        ],
        best_color_names=[
            "코랄 핑크", "살몬", "옐로우", "민트 그린",
            "피치 핑크", "골든 베이지", "로즈 핑크", "스카이 블루",
            "캐멀", "베이비 핑크", "피치", "라이트 그린",
        ],
        worst_color_names=[
            "블랙", "차콜", "버건디", "딥 퍼플",
            "그레이", "네이비",
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
            "#C8A2C8", "#87CEEB", "#DDA0DD", "#98D8C8",
            "#F0B8D0", "#A0C4E8", "#C5B4E3", "#B0C4DE",
            "#D8BFD8", "#ADD8E6", "#FFB6C1", "#E6E6FA",
        ],
        worst_colors=[
            "#FF4500", "#FF8C00", "#FFD700", "#8B4513",
            "#808000", "#FF6347",
        ],
        best_color_names=[
            "라벤더", "스카이 블루", "라일락", "민트",
            "로즈 핑크", "소프트 블루", "퍼플", "스틸 블루",
            "모브 핑크", "파우더 블루", "베이비 핑크", "라벤더 안개",
        ],
        worst_color_names=[
            "오렌지 레드", "다크 오렌지", "골드", "브라운",
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
            "#8B4513", "#CD853F", "#B8860B", "#556B2F",
            "#A0522D", "#D2691E", "#BC8F8F", "#6B8E23",
            "#DAA520", "#CC5500", "#8FBC8F", "#C19A6B",
        ],
        worst_colors=[
            "#FF69B4", "#00BFFF", "#FF1493", "#E6E6FA",
            "#87CEEB", "#FFB6C1",
        ],
        best_color_names=[
            "새들 브라운", "탄", "다크 골드", "올리브 그린",
            "시에나", "초콜릿", "로지 브라운", "올리브 드랍",
            "골든로드", "버닝 오렌지", "다크 씨 그린", "캐멀",
        ],
        worst_color_names=[
            "핫 핑크", "딥 스카이 블루", "딥 핑크", "라벤더",
            "스카이 블루", "베이비 핑크",
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
            "#DC143C", "#000000", "#FFFFFF", "#0000CD",
            "#FF0066", "#4B0082", "#00CED1", "#8B008B",
            "#228B22", "#FF1493", "#191970", "#C0C0C0",
        ],
        worst_colors=[
            "#F5DEB3", "#DEB887", "#D2B48C", "#FFDAB9",
            "#FFE4C4", "#FAF0E6",
        ],
        best_color_names=[
            "크림슨 레드", "블랙", "퓨어 화이트", "로얄 블루",
            "쇼킹 핑크", "인디고", "다크 터콰이즈", "다크 마젠타",
            "포레스트 그린", "딥 핑크", "미드나잇 네이비", "실버",
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
