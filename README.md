# Beauty AI Analyze

AI 기반 퍼스널컬러 분석 & 맞춤 뷰티/패션 추천 웹 서비스

**Live:** https://beauty-ai-analyze.onrender.com

---

## 서비스 소개

사진 한 장으로 전문 컨설턴트급 퍼스널컬러 진단을 받을 수 있는 AI 웹 서비스입니다.
얼굴 인상 분석, 컬러 드레이핑 시뮬레이션, 맞춤 뷰티/패션 제품 추천까지 무료로 제공합니다.

### 주요 기능

- **AI 퍼스널컬러 분석**: Gemini Vision API 기반, 4계절 시즌 타입 진단 + 4계절 매칭률 차트 + S/A/B/C 등급
- **얼굴 인상 분석**: 피부/눈동자/머리카락 분석, 레이더 차트(5축), 강점 및 보완 포인트
- **컬러 드레이핑 시뮬레이션**: 얼굴+컬러 배경 비교 (BEST 4 / WORST 4)
- **맞춤 제품 추천**: 성별별(남성/여성/유니섹스) 뷰티(올리브영) + 패션(무신사) 실제 제품
- **스타일링 제안**: 메이크업 포인트 카드(베이스/아이섀도/치크/립) + 추천 컬러 팔레트 3행(베이직/포인트/액센트)
- **패션 매칭**: 옷 사진 업로드 → 내 퍼스널컬러와 궁합 분석 (S/A/B/C 등급)
- **원페이지 리포트 다운로드**: 얼굴+컬러 드레이핑 비교 포함 리포트 이미지 저장
- **SNS 공유**: X(트위터), Facebook, URL 복사
- **로딩 중 퀴즈**: 분석 대기 중 연예인 퍼스널컬러 퀴즈 3문제
- **프로필 입력**: 성별, 키, 몸무게, 골격 체형(스트레이트/웨이브/내추럴), 스타일

---

## 기술 스택

| 영역 | 기술 |
|------|------|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Backend** | Python, FastAPI, Uvicorn |
| **AI 분석** | Google Gemini Vision API (모델 폴백 체인 4개) |
| **DB** | Supabase (PostgreSQL) - 분석 통계, 클릭 추적, 결과 공유 |
| **데이터** | JSON (제품 카탈로그 6파일 + 퀴즈) |
| **배포** | Render (Web Service) |
| **모니터링** | UptimeRobot (슬립 방지) |
| **분석** | Google Analytics 4 |
| **문의 시스템** | Google Sheets + Apps Script |
| **폰트** | Pretendard Variable |

---

## 프로젝트 구조

```
beauty_ai_analyze/
├── backend/
│   └── main.py                   # FastAPI 서버 (API + 정적 파일 서빙)
├── frontend/
│   ├── index.html                # 메인 SPA
│   ├── css/style.css             # 프리미엄 클린 테마
│   └── js/app.js                 # 앱 로직 (업로드, 분석, 탭, 리포트, 퀴즈, 공유)
├── analyzer/
│   ├── color_analyzer.py         # Gemini Vision API 연동 (모델 폴백 체인 + 키 이중화)
│   ├── fashion_matcher.py        # 패션 매칭 분석 (옷 사진 → 궁합)
│   ├── prompts.py                # 전문가 분석 프롬프트 (핵심 파일)
│   └── color_types.py            # 4계절 컬러 타입 정의
├── data/
│   ├── beauty_products.json      # 유니섹스 뷰티 제품 (80개)
│   ├── beauty_products_female.json
│   ├── beauty_products_male.json
│   ├── fashion_products.json     # 유니섹스 패션 제품 (37개)
│   ├── fashion_products_female.json
│   ├── fashion_products_male.json
│   ├── color_palettes.json       # 시즌별 컬러 팔레트
│   └── quiz_data.json            # 연예인 퍼스널컬러 퀴즈 (15명)
├── utils/
│   ├── image_utils.py            # 이미지 리사이즈/검증
│   └── supabase_client.py        # Supabase 연동 (통계/클릭/공유)
├── requirements.txt
├── render.yaml                   # Render 배포 설정
├── supabase_schema.sql           # Supabase 테이블 스키마
└── .env.example                  # 환경변수 템플릿
```

---

## 로컬 실행

```bash
# 1. 환경변수 설정
cp .env.example .env
# .env 파일에 GOOGLE_API_KEY, SUPABASE_URL, SUPABASE_KEY 입력

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 서버 실행
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# 4. 브라우저 접속
open http://localhost:8000
```

---

## 제품 데이터

### 뷰티 (올리브영 베스트셀러 기반)
- **립**: 롬앤 더쥬시래스팅틴트, 페리페라 잉크무드글로이틴트, 퓌 핑크옵세션, 힌스 로글로우젤틴트
- **아이**: 웨이크메이크 소프트블러링(3년1위), 클리오 프로아이팔레트에어, 홀리카홀리카, 뮤드, 3CE
- **치크**: 롬앤 베러댄치크, 크리니크 치크팝, 힌스 글로우치크, 페리페라 떡이당(화해1위)
- **베이스**: 정샘물 스킨누더쿠션(3년1위), 클리오 킬커버(6년어워즈), VDL 1등파데

### 패션 (무신사 베스트셀러 기반)
- **브랜드**: 무신사 스탠다드, 커버낫, 디스이즈네버댓
- **구매링크**: 올리브영/무신사 실제 제품 페이지 직접 연결

---

## 개인정보 보호

- 업로드된 사진은 서버에 저장되지 않으며, 분석 완료 후 즉시 삭제
- 프로필 정보는 세션 종료 시 삭제 (별도 저장 없음)
- GA4 데이터 수집은 쿠키 동의 시에만 활성화
- 상세 내용은 서비스 내 개인정보처리방침 참조

---

## 운영 비용

| 항목 | 비용 |
|------|------|
| Gemini API (무료 티어 × 2키) | $0 |
| Render 호스팅 (무료) | $0 |
| Supabase (무료) | $0 |
| UptimeRobot (무료) | $0 |
| Google Analytics 4 | $0 |
| Google Sheets (문의) | $0 |
| **총 운영 비용** | **$0/월** |

---

## API 사용량

| 항목 | 한도 |
|------|------|
| Gemini 무료 티어 일일 요청 | 1,500건 × 2키 = 3,000건 |
| 모델 폴백 체인 | 2.5-flash → 2.5-flash-lite → 2.0-flash → 3-flash-preview |
| 분석 1회당 API 호출 | 1건 |
| **일일 분석 가능 횟수** | **약 3,000회** |

---

## 업데이트 이력

| 날짜 | 내용 |
|------|------|
| 2026.05.06 | MVP 출시 - 퍼스널컬러 분석, 얼굴 인상 분석, 컬러 드레이핑, 리포트 다운로드 / 실제 제품 데이터 (올리브영 80개 + 무신사 37개, 성별별) / GA4, 개인정보처리방침, 쿠키 동의, 문의하기(Google Sheets) / Render 배포 + UptimeRobot / 프롬프트 정확도 개선 / API 호출 최적화 |
| 2026.05.06 | 모델 폴백 체인 + API 키 이중화 / 웹 UI 고도화 (4계절 비교 카드, 레이더 차트, 메이크업 포인트 카드, 컬러 팔레트 3행) / 패션 매칭 (옷 사진 → S/A/B/C) / 로딩 퀴즈 (연예인 3문제) / Supabase 연동 (통계, 클릭 추적, 공유 URL) / SNS 공유 (X, Facebook, URL 복사) / SEO + Google Search Console |
