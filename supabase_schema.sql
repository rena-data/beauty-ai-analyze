-- Beauty AI Analyze - Supabase 테이블 스키마
-- Supabase Dashboard > SQL Editor 에서 실행

-- 1. 분석 결과 저장 (통계 + URL 공유용)
CREATE TABLE analyses (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  season_type TEXT NOT NULL,
  season_detail TEXT,
  confidence REAL,
  undertone TEXT,
  season_rates JSONB,
  face_analysis JSONB,
  draping_simulation JSONB,
  best_colors JSONB,
  worst_colors JSONB,
  styling JSONB,
  one_line_conclusion TEXT,
  gender TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. 제품 클릭 추적
CREATE TABLE product_clicks (
  id BIGSERIAL PRIMARY KEY,
  season_type TEXT NOT NULL,
  gender TEXT,
  product_brand TEXT NOT NULL,
  product_name TEXT NOT NULL,
  product_category TEXT,
  clicked_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. 일별 분석 통계 뷰
CREATE VIEW daily_stats AS
SELECT
  DATE(created_at) as date,
  COUNT(*) as total_analyses,
  COUNT(*) FILTER (WHERE season_type = 'spring_warm') as spring_warm,
  COUNT(*) FILTER (WHERE season_type = 'summer_cool') as summer_cool,
  COUNT(*) FILTER (WHERE season_type = 'autumn_warm') as autumn_warm,
  COUNT(*) FILTER (WHERE season_type = 'winter_cool') as winter_cool
FROM analyses
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- 4. 인기 제품 뷰
CREATE VIEW popular_products AS
SELECT
  product_brand,
  product_name,
  product_category,
  COUNT(*) as click_count
FROM product_clicks
GROUP BY product_brand, product_name, product_category
ORDER BY click_count DESC
LIMIT 50;

-- RLS 정책 (anon 키로 INSERT만 허용, SELECT는 공유 URL용)
ALTER TABLE analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE product_clicks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can insert analyses" ON analyses FOR INSERT WITH CHECK (true);
CREATE POLICY "Anyone can read analyses by id" ON analyses FOR SELECT USING (true);

CREATE POLICY "Anyone can insert clicks" ON product_clicks FOR INSERT WITH CHECK (true);
CREATE POLICY "Anyone can read click stats" ON product_clicks FOR SELECT USING (true);
