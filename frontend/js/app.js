/* Beauty AI Analyze - Main App */

// ─── State ───
let analysisResult = null;
let selectedFile = null;
let uploadedImageDataUrl = null;

// ─── DOM ───
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

// ─── Init ───
document.addEventListener("DOMContentLoaded", () => {
    try { initUpload(); } catch(e) { console.error("initUpload:", e); }
    try { initProfile(); } catch(e) { console.error("initProfile:", e); }
    try { initTabs(); } catch(e) { console.error("initTabs:", e); }
    try { initCookieBanner(); } catch(e) { console.error("initCookieBanner:", e); }
    try { initPrivacyModal(); } catch(e) { console.error("initPrivacyModal:", e); }
    try { initContactModal(); } catch(e) { console.error("initContactModal:", e); }

    const analyzeBtn = $("#analyze-btn");
    const resetBtn = $("#reset-btn");
    const dlBtn = $("#download-report-btn");
    const shareBtn = $("#share-btn");
    if (analyzeBtn) analyzeBtn.addEventListener("click", runAnalysis);
    if (resetBtn) resetBtn.addEventListener("click", resetAll);
    if (dlBtn) dlBtn.addEventListener("click", downloadReport);
    if (shareBtn) shareBtn.addEventListener("click", copyShareUrl);

    // 공유 URL로 접속한 경우 결과 로드
    checkSharedUrl();
});

// ─── Cookie Consent ───
function initCookieBanner() {
    const banner = $("#cookie-banner");
    const consent = localStorage.getItem("cookie_consent");
    if (consent) { banner.classList.add("hidden"); return; }
    banner.classList.remove("hidden");
    $("#cookie-accept").addEventListener("click", () => {
        localStorage.setItem("cookie_consent", "accepted");
        banner.classList.add("hidden");
        // GA4 즉시 활성화
        var s = document.createElement("script");
        s.src = "https://www.googletagmanager.com/gtag/js?id=G-6ETV4L5LKK";
        document.head.appendChild(s);
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag("js", new Date());
        gtag("config", "G-6ETV4L5LKK");
    });
    $("#cookie-decline").addEventListener("click", () => {
        localStorage.setItem("cookie_consent", "declined");
        banner.classList.add("hidden");
    });
}

// ─── Contact Modal ───
const CONTACT_URL = "https://script.google.com/macros/s/AKfycbwor6iXS4G1aDSW6geAj8eMvLGRLs3l-IqoTeSidvq7WTFBZ7wYgM29g6wm2fSJVnRJ/exec";

function initContactModal() {
    const modal = $("#contact-modal");
    if (!modal) return;

    const openBtn = $("#open-contact");
    const closeBtn = $("#close-contact");
    const overlay = $("#contact-overlay");
    const submitBtn = $("#contact-submit");

    if (openBtn) openBtn.addEventListener("click", (e) => { e.preventDefault(); modal.classList.remove("hidden"); });
    if (closeBtn) closeBtn.addEventListener("click", () => closeContactModal());
    if (overlay) overlay.addEventListener("click", () => closeContactModal());
    if (submitBtn) submitBtn.addEventListener("click", submitContact);

    const domainSel = $("#contact-email-domain");
    const customInput = $("#contact-email-custom");
    if (domainSel) domainSel.addEventListener("change", () => {
        if (domainSel.value === "custom") {
            customInput.classList.remove("hidden");
            customInput.focus();
        } else {
            customInput.classList.add("hidden");
            customInput.value = "";
        }
    });
}

function closeContactModal() {
    $("#contact-modal").classList.add("hidden");
    $("#contact-status").classList.add("hidden");
}

async function submitContact() {
    const emailId = ($("#contact-email-id").value || "").trim();
    const domainSel = $("#contact-email-domain").value;
    const customDomain = ($("#contact-email-custom").value || "").trim();
    const domain = domainSel === "custom" ? customDomain : domainSel;
    const email = emailId && domain ? `${emailId}@${domain}` : "";

    const type = $("#contact-type").value;
    const content = $("#contact-content").value.trim();
    const status = $("#contact-status");
    const btn = $("#contact-submit");

    if (!emailId || !domain || !type || !content) {
        status.textContent = "모든 항목을 입력해주세요.";
        status.style.color = "#EF5350";
        status.classList.remove("hidden");
        return;
    }

    btn.disabled = true;
    btn.textContent = "전송 중...";
    status.classList.add("hidden");

    try {
        await fetch(CONTACT_URL, {
            method: "POST",
            mode: "no-cors",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, type, content }),
        });

        status.textContent = "문의가 정상적으로 접수되었습니다. 빠른 시일 내 답변드리겠습니다.";
        status.style.color = "#4CAF50";
        status.classList.remove("hidden");

        $("#contact-email-id").value = "";
        $("#contact-email-domain").value = "";
        $("#contact-email-custom").value = "";
        $("#contact-email-custom").classList.add("hidden");
        $("#contact-type").value = "";
        $("#contact-content").value = "";

        setTimeout(() => closeContactModal(), 2500);
    } catch (e) {
        status.textContent = "전송에 실패했습니다. 잠시 후 다시 시도해주세요.";
        status.style.color = "#EF5350";
        status.classList.remove("hidden");
    } finally {
        btn.disabled = false;
        btn.textContent = "문의 접수하기";
    }
}

// ─── Privacy Modal ───
function initPrivacyModal() {
    const modal = $("#privacy-modal");
    if (!modal) return;

    const openBtn = $("#open-privacy-policy");
    const closeBtn = $("#close-privacy");
    const overlay = $("#privacy-overlay");
    const termsBtn = $("#open-terms");

    if (openBtn) openBtn.addEventListener("click", (e) => { e.preventDefault(); modal.classList.remove("hidden"); });
    if (closeBtn) closeBtn.addEventListener("click", () => modal.classList.add("hidden"));
    if (overlay) overlay.addEventListener("click", () => modal.classList.add("hidden"));
    if (termsBtn) termsBtn.addEventListener("click", (e) => { e.preventDefault(); modal.classList.remove("hidden"); });
}

// ─── Hex to Color Chip ───
function hexToChip(text) {
    if (!text) return "";
    return text.replace(/#([0-9A-Fa-f]{6})\b/g, (match) =>
        `<span style="display:inline-block;width:14px;height:14px;border-radius:4px;border:1px solid #ddd;background-color:${match};vertical-align:middle;margin:0 2px;"></span>`
    );
}

// ─── Product Click Tracking (Supabase + GA4) ───
function trackClick(brand, name, category) {
    gEvent("product_click", { brand, product: name });
    const r = analysisResult;
    if (!r) return;
    fetch("/api/track-click", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            season_type: r.season_type,
            gender: (document.getElementById("prof-gender") || {}).value || "",
            brand, name, category,
        }),
    }).catch(() => {});
}

// ─── Share URL ───
function getShareUrl() {
    if (!analysisResult || !analysisResult.share_id) return null;
    return `${location.origin}?share=${analysisResult.share_id}`;
}

// ─── Share URL Copy ───
function copyShareUrl() {
    const url = getShareUrl();
    if (!url) { alert("공유 링크를 생성할 수 없습니다."); return; }
    navigator.clipboard.writeText(url).then(() => {
        const btn = $("#share-btn");
        btn.textContent = "링크 복사됨!";
        setTimeout(() => { btn.textContent = "결과 공유 링크 복사"; }, 2000);
    }).catch(() => {
        prompt("아래 링크를 복사하세요:", url);
    });
}

// ─── Shared URL Load ───
async function checkSharedUrl() {
    const params = new URLSearchParams(location.search);
    const shareId = params.get("share");
    if (!shareId) return;

    try {
        const resp = await fetch(`/api/share/${shareId}`);
        if (!resp.ok) return;
        analysisResult = await resp.json();
        renderResults();
        // 공유 결과는 업로드 섹션 숨기기
        $("#upload-section").classList.add("hidden");
    } catch { }
}

// ─── GA4 Event Helper ───
function gEvent(name, params) {
    if (typeof gtag === "function") gtag("event", name, params || {});
}

// ─── Upload ───
function initUpload() {
    const zone = $("#drop-zone");
    const input = $("#file-input");
    zone.addEventListener("click", () => input.click());
    input.addEventListener("change", (e) => handleFile(e.target.files[0]));
    zone.addEventListener("dragover", (e) => { e.preventDefault(); zone.classList.add("dragover"); });
    zone.addEventListener("dragleave", () => zone.classList.remove("dragover"));
    zone.addEventListener("drop", (e) => {
        e.preventDefault();
        zone.classList.remove("dragover");
        handleFile(e.dataTransfer.files[0]);
    });
}

function handleFile(file) {
    if (!file) return;
    const valid = ["image/jpeg", "image/png", "image/webp"];
    if (!valid.includes(file.type)) { showError("지원하지 않는 파일 형식입니다."); return; }
    if (file.size > 10 * 1024 * 1024) { showError("파일 크기가 10MB를 초과합니다."); return; }
    selectedFile = file;
    const reader = new FileReader();
    reader.onload = (e) => {
        uploadedImageDataUrl = e.target.result;
        const img = $("#preview-img");
        img.src = uploadedImageDataUrl;
        img.classList.remove("hidden");
        $("#upload-placeholder").classList.add("hidden");
    };
    reader.readAsDataURL(file);
    $("#analyze-btn").disabled = false;
    hideError();
}

// ─── Profile ───
function initProfile() {
    // 키, 몸무게 모두 HTML에 정적으로 정의됨
}

// ─── Analysis ───
async function runAnalysis() {
    if (!selectedFile) return;
    $("#upload-section").classList.add("hidden");
    $("#loading-section").classList.remove("hidden");
    $("#results-section").classList.add("hidden");
    hideError();

    // 로딩 스텝 애니메이션
    const steps = [$("#step-1"), $("#step-2"), $("#step-3"), $("#step-4")];
    steps.forEach(s => { if(s) { s.className = "loading-step"; } });
    if(steps[0]) steps[0].classList.add("active");
    const stepTimer = setInterval(() => {
        const cur = steps.findIndex(s => s && s.classList.contains("active"));
        if (cur >= 0 && cur < steps.length - 1) {
            steps[cur].classList.remove("active");
            steps[cur].classList.add("done");
            steps[cur + 1].classList.add("active");
        }
    }, 3000);

    // 로딩 중 퀴즈 표시
    showLoadingQuiz();

    const form = new FormData();
    form.append("file", selectedFile);
    try {
        const resp = await fetch("/api/analyze", { method: "POST", body: form });
        if (!resp.ok) { const err = await resp.json(); throw new Error(err.detail || "분석 중 오류가 발생했습니다."); }
        analysisResult = await resp.json();
        gEvent("analysis_complete", { season_type: analysisResult.season_type });
        renderResults();
    } catch (e) {
        showError(e.message);
        $("#upload-section").classList.remove("hidden");
    } finally {
        clearInterval(stepTimer);
        $("#loading-section").classList.add("hidden");
    }
}

// ─── Tabs ───
function initTabs() {
    $("#tabs").addEventListener("click", (e) => {
        if (!e.target.classList.contains("tab")) return;
        $$(".tab").forEach((t) => t.classList.remove("active"));
        e.target.classList.add("active");
        renderTab(e.target.dataset.tab);
    });
}

// ─── Reset ───
function resetAll() {
    analysisResult = null; selectedFile = null; uploadedImageDataUrl = null;
    $("#file-input").value = "";
    $("#preview-img").classList.add("hidden");
    $("#preview-img").src = "";
    $("#upload-placeholder").classList.remove("hidden");
    $("#upload-section").classList.remove("hidden");
    $("#results-section").classList.add("hidden");
    $("#analyze-btn").disabled = true;
    hideError();
}

// ─── Error ───
function showError(msg) { const el = $("#error-msg"); el.textContent = msg; el.classList.remove("hidden"); }
function hideError() { $("#error-msg").classList.add("hidden"); }

// ─── Season helpers ───
const SM = {
    spring_warm: { emoji: "🌸", ko: "봄 웜톤", en: "Spring Warm", cls: "spring", accent: "#FF8FAB", vibe: "화사한 생기와 따뜻한 에너지" },
    summer_cool: { emoji: "🌊", ko: "여름 쿨톤", en: "Summer Cool", cls: "summer", accent: "#C8A2C8", vibe: "부드러운 우아함과 차분한 세련미" },
    autumn_warm: { emoji: "🍂", ko: "가을 웜톤", en: "Autumn Warm", cls: "autumn", accent: "#CD853F", vibe: "깊은 고급스러움과 풍요로운 무드" },
    winter_cool: { emoji: "❄️", ko: "겨울 쿨톤", en: "Winter Cool", cls: "winter", accent: "#DC143C", vibe: "강렬한 카리스마와 시크한 존재감" },
};

// ─── Grade helper ───
function getGrade(conf) {
    if (conf >= 80) return { grade: "S", label: "매우 높음", color: "#4CAF50" };
    if (conf >= 65) return { grade: "A", label: "높음", color: "#2196F3" };
    if (conf >= 50) return { grade: "B", label: "보통", color: "#FF9800" };
    return { grade: "C", label: "낮음", color: "#EF5350" };
}
function fmt(n) { return n.toLocaleString("ko-KR"); }

// ─── Render Results ───
function renderResults() {
    const r = analysisResult;
    const s = SM[r.season_type] || SM.spring_warm;
    const conf = Math.round((r.confidence || 0) * 100);
    const confCls = conf >= 75 ? "conf-high" : conf >= 50 ? "conf-mid" : "conf-low";
    const detail = r.season_detail || s.ko;
    const conclusion = r.one_line_conclusion || "";

    // Result header with face photo
    const faceImg = uploadedImageDataUrl
        ? `<img src="${uploadedImageDataUrl}" class="result-face-img" alt="분석 사진">`
        : "";

    const g = getGrade(conf);
    const rates = r.season_rates || {};

    // 4계절 매칭률 차트 (프롬프트에서 반환 시)
    const seasons = [
        { key: "spring_warm", ...SM.spring_warm },
        { key: "summer_cool", ...SM.summer_cool },
        { key: "autumn_warm", ...SM.autumn_warm },
        { key: "winter_cool", ...SM.winter_cool },
    ];
    const hasRates = Object.keys(rates).length > 0;
    const rateChart = hasRates ? `
        <div style="margin-top:1rem;">
            <div style="font-size:0.85rem;font-weight:600;margin-bottom:0.5rem;">4계절 매칭률</div>
            ${seasons.map(ss => {
                const pct = rates[ss.key] || 0;
                const isTop = ss.key === r.season_type;
                return `<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.4rem;">
                    <span style="font-size:0.75rem;width:60px;color:${isTop ? ss.accent : 'var(--text-sub)'};font-weight:${isTop ? '700' : '400'};">${ss.emoji} ${ss.ko.slice(0,2)}</span>
                    <div style="flex:1;height:8px;background:#F0F0F0;border-radius:4px;overflow:hidden;">
                        <div style="width:${pct}%;height:100%;background:${ss.accent};border-radius:4px;transition:width 0.8s;"></div>
                    </div>
                    <span style="font-size:0.75rem;width:32px;text-align:right;color:${isTop ? ss.accent : 'var(--text-sub)'};font-weight:${isTop ? '700' : '400'};">${pct}%</span>
                </div>`;
            }).join("")}
        </div>` : "";

    $("#result-header").innerHTML = `
        <div class="result-header-with-face">
            ${faceImg}
            <div class="result-header-info">
                <div class="result-header-inner">
                    <span class="season-badge season-${s.cls}">${s.emoji} ${detail}</span>
                    <span style="display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:50%;background:${g.color};color:white;font-weight:800;font-size:0.8rem;margin-left:0.5rem;" title="분석 등급: ${g.label}">${g.grade}</span>
                    <span style="color:var(--text-sub);font-size:0.85rem;margin-left:0.3rem;">${s.en}</span>
                </div>
                <div style="font-size:0.85rem;color:${s.accent};margin-top:0.4rem;font-style:italic;">${s.vibe}</div>
                <div style="margin-top:0.8rem;">
                    <div style="display:flex;justify-content:space-between;font-size:0.85rem;">
                        <span style="font-weight:600;">분석 확신도</span>
                        <span style="color:var(--text-sub);">${conf}% (${g.label})</span>
                    </div>
                    <div class="conf-bar"><div class="conf-fill ${confCls}" style="width:${conf}%"></div></div>
                </div>
                ${rateChart}
                ${conclusion ? `<div class="conclusion-box"><strong>한 줄 결론</strong> ${conclusion}</div>` : ""}
            </div>
        </div>`;

    $("#results-section").classList.remove("hidden");
    // 공유 버튼 표시
    const shareBtn = $("#share-btn");
    if (shareBtn && analysisResult.share_id) shareBtn.style.display = "inline-block";
    $$(".tab").forEach((t) => t.classList.remove("active"));
    $$(".tab")[0].classList.add("active");
    renderTab("draping");
    $("#results-section").scrollIntoView({ behavior: "smooth", block: "start" });
}

// ─── Tab Renderer ───
function renderTab(tab) {
    const el = $("#tab-content");
    const r = analysisResult;
    if (!r) return;
    switch (tab) {
        case "draping": el.innerHTML = renderDraping(r); break;
        case "face": el.innerHTML = renderFace(r); break;
        case "palette": renderPalette(el, r); break;
        case "styling": el.innerHTML = renderStyling(r); break;
        case "beauty": renderProducts(el, r, "beauty"); break;
        case "fashion": renderProducts(el, r, "fashion"); break;
        case "detail": el.innerHTML = renderDetail(r); break;
        case "fashion-match": el.innerHTML = renderFashionMatch(r); initFashionMatchUpload(); break;
    }
}

// ── Draping (1-1a: 4계절 비교 카드 + 드레이핑) ──
function renderDraping(r) {
    const d = r.draping_simulation || {};
    const goodC = d.good_colors || [];
    const badC = d.bad_colors || [];
    const rates = r.season_rates || {};
    const keywords = r.season_keywords || {};
    const faceUrl = uploadedImageDataUrl || "";

    // 4계절 비교 카드
    const seasonCards = [
        { key: "spring_warm", ...SM.spring_warm },
        { key: "summer_cool", ...SM.summer_cool },
        { key: "autumn_warm", ...SM.autumn_warm },
        { key: "winter_cool", ...SM.winter_cool },
    ].map(ss => {
        const pct = rates[ss.key] || 0;
        const isTop = ss.key === r.season_type;
        const stars = Math.round(pct / 20);
        const kw = keywords[ss.key] || ss.vibe;
        const matchLabel = pct >= 80 ? "매우 잘 어울림" : pct >= 60 ? "잘 어울림" : pct >= 40 ? "보통" : "덜 어울림";
        return `<div style="text-align:center;padding:0.6rem;border-radius:12px;border:2px solid ${isTop ? ss.accent : '#E8E8E8'};background:${isTop ? ss.accent+'10' : '#fff'};position:relative;min-width:0;">
            ${isTop ? '<div style="position:absolute;top:-10px;left:50%;transform:translateX(-50%);background:'+ss.accent+';color:white;font-size:0.65rem;font-weight:700;padding:2px 8px;border-radius:10px;">BEST MATCH</div>' : ''}
            <div style="width:100%;height:80px;background:${ss.accent};border-radius:8px;display:flex;align-items:flex-end;justify-content:center;overflow:hidden;margin-top:${isTop?'4px':'0'};">
                ${faceUrl ? `<img src="${faceUrl}" style="width:60px;height:60px;object-fit:cover;border-radius:50%;border:2px solid white;margin-bottom:4px;">` : ''}
            </div>
            <div style="font-size:0.75rem;font-weight:700;color:${ss.accent};margin-top:0.4rem;">${ss.emoji} ${ss.ko}</div>
            <div style="font-size:0.65rem;color:var(--text-sub);margin-top:0.15rem;">${kw}</div>
            <div style="font-size:0.7rem;color:#FFB300;margin-top:0.2rem;">${'★'.repeat(stars)}${'☆'.repeat(5-stars)}</div>
            <div style="font-size:0.62rem;color:var(--text-sub);">어울림: ${matchLabel}</div>
        </div>`;
    }).join("");

    // 드레이핑 Best/Worst with face
    const drapCard = (c, border) => `<div style="text-align:center;flex:1;min-width:0;">
        <div style="height:70px;background:${c.hex};border-radius:8px;display:flex;align-items:flex-end;justify-content:center;border:2px solid ${border};">
            ${faceUrl ? `<img src="${faceUrl}" style="width:50px;height:50px;object-fit:cover;border-radius:50%;border:2px solid white;margin-bottom:4px;">` : ''}
        </div>
        <div style="font-size:0.72rem;font-weight:700;margin-top:4px;">${c.color}</div>
        <div style="font-size:0.65rem;color:var(--text-sub);line-height:1.3;margin-top:2px;">${c.effect}</div>
    </div>`;

    // Best/Worst 큰 컬러바 (1-2)
    const best = r.best_colors || [], worst = r.worst_colors || [];
    const colorBarItem = (c) => `<div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.5rem;">
        <div style="width:60px;height:20px;border-radius:6px;background:${c.hex};border:1px solid #e0e0e0;flex-shrink:0;"></div>
        <span style="font-size:0.8rem;font-weight:600;">${c.color}</span>
        <span style="font-size:0.72rem;color:var(--text-sub);">${c.reason || ''}</span>
    </div>`;

    return `
    <!-- 4계절 비교 -->
    <div class="card">
        <h3 class="section-title">4계절 비교</h3>
        <p class="section-sub">가장 잘 어울리는 컬러를 찾아보세요.</p>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.6rem;">${seasonCards}</div>
    </div>

    <!-- 컬러 드레이핑 -->
    <div class="card" style="margin-top:1rem;">
        <h3 class="section-title">컬러 드레이핑 시뮬레이션</h3>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;">
            <div>
                <p style="font-weight:700;color:var(--green);margin-bottom:0.8rem;font-size:0.9rem;">잘 어울리는 컬러 (BEST 4)</p>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;">${goodC.slice(0,4).map(c => drapCard(c,'#4CAF50')).join('')}</div>
            </div>
            <div>
                <p style="font-weight:700;color:var(--red);margin-bottom:0.8rem;font-size:0.9rem;">안 어울리는 컬러 (WORST 4)</p>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;">${badC.slice(0,4).map(c => drapCard(c,'#EF5350')).join('')}</div>
            </div>
        </div>
    </div>

    <!-- 추천 & 비추천 컬러 바 -->
    ${best.length ? `<div class="card" style="margin-top:1rem;">
        <h3 class="section-title">추천 & 피해야 할 컬러</h3>
        <div class="colors-grid">
            <div>
                <p style="font-weight:700;color:var(--green);margin-bottom:0.6rem;">BEST 5</p>
                ${best.map(colorBarItem).join('')}
            </div>
            <div>
                <p style="font-weight:700;color:var(--red);margin-bottom:0.6rem;">WORST</p>
                ${worst.map(colorBarItem).join('')}
            </div>
        </div>
    </div>` : ''}`;
}

// ── Face (1-1b: 레이더 차트 + 개선) ──
function drawRadarSVG(radar) {
    if (!radar) return "";
    const labels = ["밝기","채도","대비","온기","선명도"];
    const keys = ["brightness","saturation","contrast","warmth","clarity"];
    const vals = keys.map(k => (radar[k] || 3));
    const cx = 80, cy = 80, R = 60;
    const angleStep = (2 * Math.PI) / 5;
    const startAngle = -Math.PI / 2;

    // 배경 오각형 (5단계)
    let bgLines = "";
    for (let lv = 1; lv <= 5; lv++) {
        const r = R * lv / 5;
        const pts = Array.from({length:5}, (_,i) => {
            const a = startAngle + i * angleStep;
            return `${cx + r*Math.cos(a)},${cy + r*Math.sin(a)}`;
        }).join(" ");
        bgLines += `<polygon points="${pts}" fill="none" stroke="#E8E8E8" stroke-width="0.5"/>`;
    }

    // 축 선
    let axisLines = "";
    for (let i = 0; i < 5; i++) {
        const a = startAngle + i * angleStep;
        axisLines += `<line x1="${cx}" y1="${cy}" x2="${cx+R*Math.cos(a)}" y2="${cy+R*Math.sin(a)}" stroke="#E8E8E8" stroke-width="0.5"/>`;
    }

    // 데이터 폴리곤
    const dataPts = vals.map((v, i) => {
        const r = R * v / 5;
        const a = startAngle + i * angleStep;
        return `${cx + r*Math.cos(a)},${cy + r*Math.sin(a)}`;
    }).join(" ");

    // 라벨
    const labelEls = labels.map((lb, i) => {
        const a = startAngle + i * angleStep;
        const lr = R + 18;
        const x = cx + lr * Math.cos(a);
        const y = cy + lr * Math.sin(a);
        return `<text x="${x}" y="${y}" text-anchor="middle" dominant-baseline="middle" font-size="8" fill="#6B6B6B" font-weight="600">${lb}</text>`;
    }).join("");

    return `<svg viewBox="0 0 160 160" style="width:160px;height:160px;">
        ${bgLines}${axisLines}
        <polygon points="${dataPts}" fill="rgba(232,160,191,0.25)" stroke="#E8A0BF" stroke-width="1.5"/>
        ${labelEls}
    </svg>`;
}

function renderFace(r) {
    const f = r.face_analysis || {};
    const radar = r.face_radar || {};
    const faceUrl = uploadedImageDataUrl || "";
    const radarSVG = drawRadarSVG(radar);

    return `<div class="card">
        <h3 class="section-title">얼굴 인상 분석</h3>
        <div style="display:flex;gap:1.5rem;align-items:flex-start;margin-bottom:1.5rem;">
            ${faceUrl ? `<img src="${faceUrl}" style="width:140px;height:140px;object-fit:cover;border-radius:16px;border:3px solid var(--border);flex-shrink:0;">` : ''}
            <div style="flex:1;">
                <div class="face-grid" style="margin-bottom:0;">
                    <div class="analysis-block" style="border-left-color:#FFB6C1"><strong>피부</strong>${hexToChip(f.skin)}</div>
                    <div class="analysis-block" style="border-left-color:#87CEEB"><strong>눈동자</strong>${hexToChip(f.eyes)}</div>
                    <div class="analysis-block" style="border-left-color:#DEB887"><strong>머리카락</strong>${hexToChip(f.hair)}</div>
                    <div class="analysis-block" style="border-left-color:#C0C0C0"><strong>대비감</strong>${hexToChip(f.face_contrast)}</div>
                </div>
            </div>
        </div>
        <div style="display:flex;gap:1.5rem;align-items:flex-start;">
            ${radarSVG ? `<div style="text-align:center;flex-shrink:0;">
                <div style="font-size:0.8rem;font-weight:700;margin-bottom:0.3rem;">얼굴 분석 차트</div>
                ${radarSVG}
            </div>` : ''}
            <div style="flex:1;">
                <div class="strength-box" style="margin-bottom:0.6rem;"><h4>나의 강점</h4><ul>${(f.strengths || []).map(s => `<li>${s}</li>`).join("") || "<li>-</li>"}</ul></div>
                <div class="improve-box"><h4>보완 포인트</h4><ul>${(f.improvements || []).map(s => `<li>${s}</li>`).join("") || "<li>-</li>"}</ul></div>
            </div>
        </div>
    </div>`;
}

// ── Palette ──
async function renderPalette(el, r) {
    el.innerHTML = `<div class="card"><div class="loading-content"><div class="spinner"></div></div></div>`;
    try {
        const resp = await fetch(`/api/palettes/${r.season_type}`);
        const data = await resp.json();
        const s = SM[r.season_type];
        const sw = (arr) => (arr || []).map((c) => `<div class="swatch"><div class="swatch-tooltip">${c.name} (${c.hex})</div><div class="swatch-color" style="background:${c.hex}"></div><div class="swatch-name">${c.name}</div></div>`).join("");
        el.innerHTML = `<div class="card">
            <h3 class="section-title">${s.emoji} ${data.name || s.ko} 컬러 팔레트</h3>
            <p style="font-weight:700;color:var(--green);margin-bottom:0.8rem;">Best Colors</p>
            <div class="palette-wrap">${sw(data.best)}</div>
            <hr style="border:none;border-top:1px solid var(--border);margin:1.5rem 0;">
            <p style="font-weight:700;color:var(--red);margin-bottom:0.8rem;">Worst Colors</p>
            <div class="palette-wrap">${sw(data.worst)}</div></div>`;
    } catch { el.innerHTML = `<div class="card"><p>팔레트를 불러올 수 없습니다.</p></div>`; }
}

// ── Styling (1-1c: 메이크업 포인트 + 1-1d: 팔레트 3행 + 1-3: 패션 원형칩) ──
function renderStyling(r) {
    const st = r.styling || {}, s = SM[r.season_type] || {};
    const cp = r.color_palette || {};

    // 메이크업 포인트 카드 (아이콘 + 설명)
    const makeupCards = [
        { icon: "💧", label: "베이스", text: st.makeup_base || "" },
        { icon: "👁", label: "아이섀도", text: st.makeup_eyeshadow || "" },
        { icon: "🩷", label: "치크", text: st.makeup_blush || "" },
        { icon: "💋", label: "립", text: st.makeup_lip || "" },
    ].map(m => `<div style="background:var(--bg);border-radius:12px;padding:0.8rem;text-align:center;">
        <div style="font-size:1.5rem;margin-bottom:0.3rem;">${m.icon}</div>
        <div style="font-size:0.8rem;font-weight:700;margin-bottom:0.3rem;">${m.label}</div>
        <div style="font-size:0.75rem;color:var(--text-sub);line-height:1.5;">${hexToChip(m.text)}</div>
    </div>`).join("");

    // 컬러 팔레트 3행 (원형 칩)
    const paletteRow = (label, colors) => {
        if (!colors || !colors.length) return "";
        return `<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
            <span style="font-size:0.75rem;font-weight:700;width:50px;flex-shrink:0;color:var(--text-sub);">${label}</span>
            <div style="display:flex;gap:6px;flex-wrap:wrap;">
                ${colors.map(c => `<div style="text-align:center;" title="${c.color}">
                    <div style="width:28px;height:28px;border-radius:50%;background:${c.hex};border:2px solid #e0e0e0;"></div>
                </div>`).join("")}
            </div>
        </div>`;
    };
    const paletteHtml = (cp.basic || cp.point || cp.accent) ? `
        <div style="margin-top:1rem;">
            <p style="font-weight:700;margin-bottom:0.6rem;">추천 컬러 팔레트</p>
            <div style="background:var(--bg);border-radius:12px;padding:1rem;">
                ${paletteRow("베이직", cp.basic)}
                ${paletteRow("포인트", cp.point)}
                ${paletteRow("액센트", cp.accent)}
            </div>
        </div>` : "";

    return `<div class="card">
        <h3 class="section-title">스타일링 제안</h3>

        <p style="font-weight:700;margin-bottom:0.8rem;">메이크업 포인트</p>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.6rem;margin-bottom:1.2rem;">
            ${makeupCards}
        </div>

        <p style="font-weight:700;margin-bottom:0.8rem;">헤어컬러</p>
        <div class="hair-grid">
            <div class="hair-good"><p>추천</p><p style="font-size:0.85rem;line-height:1.6">${hexToChip(st.hair_recommended)}</p></div>
            <div class="hair-bad"><p>피하기</p><p style="font-size:0.85rem;line-height:1.6">${hexToChip(st.hair_avoid)}</p></div>
        </div>

        <p style="font-weight:700;margin-bottom:0.8rem;">패션 색 조합</p>
        <div class="analysis-block" style="border-left-color:${s.accent || 'var(--primary)'}">${hexToChip(st.fashion_combinations)}</div>

        ${paletteHtml}
    </div>`;
}

// ── Products ──
const BEAUTY_CATS = { lip: "Lip — 립 메이크업", eye: "Eye — 아이 메이크업", cheek: "Cheek — 치크 & 블러셔", base: "Base — 베이스 메이크업" };
const FASHION_CATS = { top: "Top — 상의", bottom: "Bottom — 하의", outer: "Outer — 아우터" };
const BC = { "롬앤":"#FF6B6B","페리페라":"#FF8FAB","클리오":"#8B6914","맥":"#000","에스티 로더":"#002D5F","라네즈":"#0077B6","샤넬":"#000","디올":"#1A1A1A","UNIQLO":"#E60012","ZARA":"#000","COS":"#333","H&M":"#E50010","MANGO":"#000" };

function productCard(item, type) {
    const brand = item.brand || "";
    const colorHex = item.color_hex || BC[brand] || "#6B6B6B";
    const hasImg = item.image_url && item.image_url.length > 5;
    const buyUrl = item.buy_url || "";

    const imgInner = hasImg
        ? `<img src="${item.image_url}" style="width:100%;height:100%;object-fit:contain;padding:8px;background:#fff;" alt="${item.name}" onerror="this.parentElement.innerHTML='<div class=product-img-overlay><span class=brand-text>${brand}</span><span class=product-text>${item.name.slice(0,18)}</span></div>'">`
        : `<div class="product-img-overlay"><span class="brand-text">${brand}</span><span class="product-text">${item.name.length > 20 ? item.name.slice(0,20)+"..." : item.name}</span></div>`;

    const dot = type === "fashion" && item.color_hex ? `<span class="fashion-color" style="background:${item.color_hex}"></span>` : "";
    const buyBtn = buyUrl ? `<a href="${buyUrl}" target="_blank" rel="noopener" class="buy-link" onclick="trackClick('${brand}','${item.name.replace(/'/g,"")}','${item.category||""}')">구매하기 →</a>` : "";

    return `<div class="product-card">
        <div class="product-img" style="background:linear-gradient(135deg,${colorHex}22,${colorHex}11);">${imgInner}</div>
        <div class="product-body">
            <div class="product-brand">${brand}</div>
            <div class="product-name">${dot}${item.name}</div>
            <div class="product-price">${fmt(item.price)}원</div>
            <div class="product-reason">${item.reason}</div>
            ${buyBtn}
        </div></div>`;
}

async function renderProducts(el, r, type) {
    el.innerHTML = `<div class="card"><div class="loading-content"><div class="spinner"></div></div></div>`;
    try {
        const gender = (document.getElementById("prof-gender") || {}).value || "";
        const resp = await fetch(`/api/products/${r.season_type}?gender=${gender}`);
        const data = await resp.json();
        const products = data[type] || {};
        const cats = type === "beauty" ? BEAUTY_CATS : FASHION_CATS;
        let html = `<div class="card">
            <h3 class="section-title">${type === "beauty" ? "추천 뷰티 제품" : "추천 패션 아이템"}</h3>
            <p class="section-sub">당신의 퍼스널컬러에 딱 맞는 ${type === "beauty" ? "제품" : "아이템"}들을 엄선했어요.</p>`;
        for (const [key, label] of Object.entries(cats)) {
            const items = (products[key] || []).slice(0, 3);
            if (!items.length) continue;
            html += `<div class="product-category"><h4>${label}</h4><div class="product-grid">${items.map((it) => productCard(it, type)).join("")}</div></div>`;
        }
        el.innerHTML = html + `</div>`;
    } catch { el.innerHTML = `<div class="card"><p>제품 정보를 불러올 수 없습니다.</p></div>`; }
}

// ── Detail ──
function renderDetail(r) {
    const s = SM[r.season_type] || {};
    const ut = r.undertone || "";
    const shortUt = ut.includes("(") ? ut.split("(")[0].trim() : ut;
    return `<div class="card">
        <h3 class="section-title">퍼스널컬러 상세 분석</h3>
        <div class="metric-grid">
            <div class="metric-card"><div class="metric-label">언더톤</div><div class="metric-value">${shortUt}</div></div>
            <div class="metric-card"><div class="metric-label">대비감</div><div class="metric-value">${r.contrast_level || "중간"}</div></div>
            <div class="metric-card"><div class="metric-label">시즌 타입</div><div class="metric-value">${s.emoji} ${r.season_detail || s.ko}</div></div>
        </div>
        ${r.undertone_reason ? `<div class="analysis-block" style="border-left-color:var(--primary)"><strong>언더톤 판정 근거</strong>${r.undertone_reason}</div>` : ""}
        <div class="analysis-block"><strong>피부톤 특성</strong>${r.skin_description || ""}</div>
        <div class="analysis-block"><strong>분석 근거</strong>${r.analysis_reasoning || ""}</div>
        ${r.celebrity_reference ? `<div class="analysis-block" style="border-left-color:#FFD700"><strong>비슷한 퍼스널컬러의 연예인</strong>${r.celebrity_reference}</div>` : ""}
        ${r.special_notes ? `<div class="analysis-block" style="border-left-color:#C0C0C0"><strong>참고사항</strong>${r.special_notes}</div>` : ""}
    </div>`;
}

// ── Fashion Match (2-1) ──
function renderFashionMatch(r) {
    const s = SM[r.season_type] || SM.spring_warm;
    return `<div class="card">
        <h3 class="section-title">옷 매칭 분석</h3>
        <p class="section-sub">옷 사진을 업로드하면 내 퍼스널컬러(${s.emoji} ${r.season_detail || s.ko})와 얼마나 어울리는지 AI가 분석합니다.</p>

        <div id="fashion-match-upload" style="border:2px dashed var(--border);border-radius:12px;padding:2rem;text-align:center;cursor:pointer;transition:border-color 0.3s;margin-bottom:1rem;">
            <input type="file" id="fashion-file-input" accept="image/jpeg,image/png,image/webp" hidden>
            <div id="fashion-upload-placeholder">
                <div style="font-size:2rem;margin-bottom:0.5rem;">👗</div>
                <p style="color:var(--text-sub);font-size:0.9rem;">옷 사진을 드래그하거나 클릭하여 업로드</p>
                <span style="font-size:0.75rem;color:#aaa;">상의, 하의, 아우터, 원피스 등</span>
            </div>
            <img id="fashion-preview" class="hidden" style="max-height:200px;border-radius:8px;">
        </div>

        <button id="fashion-match-btn" class="btn-primary" disabled style="margin-bottom:1rem;">👗 매칭 분석 시작</button>

        <div id="fashion-match-loading" class="hidden" style="text-align:center;padding:1rem;">
            <div class="spinner"></div>
            <p style="color:var(--text-sub);margin-top:0.5rem;font-size:0.85rem;">옷 색상 분석 중...</p>
        </div>

        <div id="fashion-match-result"></div>
    </div>`;
}

function initFashionMatchUpload() {
    const zone = $("#fashion-match-upload");
    const input = $("#fashion-file-input");
    const btn = $("#fashion-match-btn");
    if (!zone || !input || !btn) return;

    zone.addEventListener("click", () => input.click());
    input.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (ev) => {
            const img = $("#fashion-preview");
            img.src = ev.target.result;
            img.classList.remove("hidden");
            $("#fashion-upload-placeholder").classList.add("hidden");
            btn.disabled = false;
        };
        reader.readAsDataURL(file);
    });

    zone.addEventListener("dragover", (e) => { e.preventDefault(); zone.style.borderColor = "var(--primary)"; });
    zone.addEventListener("dragleave", () => { zone.style.borderColor = "var(--border)"; });
    zone.addEventListener("drop", (e) => {
        e.preventDefault();
        zone.style.borderColor = "var(--border)";
        input.files = e.dataTransfer.files;
        input.dispatchEvent(new Event("change"));
    });

    btn.addEventListener("click", runFashionMatch);
}

async function runFashionMatch() {
    const input = $("#fashion-file-input");
    const file = input.files[0];
    if (!file) return;

    const btn = $("#fashion-match-btn");
    const loading = $("#fashion-match-loading");
    const resultEl = $("#fashion-match-result");

    btn.disabled = true;
    btn.textContent = "분석 중...";
    loading.classList.remove("hidden");
    resultEl.innerHTML = "";

    const form = new FormData();
    form.append("file", file);
    form.append("season_type", analysisResult.season_type);

    try {
        const resp = await fetch("/api/fashion-match", { method: "POST", body: form });
        if (!resp.ok) {
            const err = await resp.json();
            throw new Error(err.detail || "매칭 분석 중 오류가 발생했습니다.");
        }
        const result = await resp.json();
        gEvent("fashion_match", { season_type: analysisResult.season_type, grade: result.match_grade });
        resultEl.innerHTML = renderFashionMatchResult(result);
    } catch (e) {
        resultEl.innerHTML = `<div class="error-msg">${e.message}</div>`;
    } finally {
        loading.classList.add("hidden");
        btn.disabled = false;
        btn.textContent = "👗 매칭 분석 시작";
    }
}

function renderFashionMatchResult(result) {
    const score = result.match_score || 0;
    const grade = result.match_grade || "B";
    const gradeColors = { S: "#4CAF50", A: "#2196F3", B: "#FF9800", C: "#EF5350" };
    const gradeLabels = { S: "매우 잘 어울림", A: "잘 어울림", B: "보통", C: "안 어울림" };
    const gc = gradeColors[grade] || "#999";

    const dominantColors = (result.dominant_colors || []).map(c =>
        `<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.3rem;">
            <div style="width:28px;height:28px;border-radius:6px;background:${c.hex};border:1px solid #ddd;"></div>
            <span style="font-size:0.85rem;font-weight:600;">${c.color}</span>
            <span style="font-size:0.75rem;color:var(--text-sub);">${c.percentage}%</span>
        </div>`).join("");

    const seasonBars = Object.entries(result.season_match || {}).map(([key, pct]) => {
        const ss = SM[key] || {};
        const isTop = key === result.best_season;
        return `<div style="display:flex;align-items:center;gap:0.4rem;margin-bottom:0.3rem;">
            <span style="font-size:0.72rem;width:50px;color:${isTop ? ss.accent : 'var(--text-sub)'};font-weight:${isTop ? '700' : '400'};">${ss.emoji || ''} ${(ss.ko || '').slice(0,2)}</span>
            <div style="flex:1;height:8px;background:#F0F0F0;border-radius:4px;overflow:hidden;">
                <div style="width:${pct}%;height:100%;background:${ss.accent || '#ccc'};border-radius:4px;"></div>
            </div>
            <span style="font-size:0.72rem;width:30px;text-align:right;">${pct}%</span>
        </div>`;
    }).join("");

    return `
    <div style="border:2px solid ${gc};border-radius:12px;overflow:hidden;">
        <!-- Grade Header -->
        <div style="background:${gc};color:white;padding:0.8rem 1.2rem;display:flex;justify-content:space-between;align-items:center;">
            <div>
                <span style="font-size:1.5rem;font-weight:800;">${grade}</span>
                <span style="font-size:0.9rem;margin-left:0.5rem;">${gradeLabels[grade] || ''}</span>
            </div>
            <div style="font-size:1.2rem;font-weight:700;">${score}점</div>
        </div>

        <div style="padding:1.2rem;">
            <!-- Dominant Colors -->
            <div style="margin-bottom:1rem;">
                <p style="font-weight:700;font-size:0.85rem;margin-bottom:0.5rem;">감지된 색상</p>
                ${dominantColors}
            </div>

            <!-- Season Match -->
            <div style="margin-bottom:1rem;">
                <p style="font-weight:700;font-size:0.85rem;margin-bottom:0.5rem;">시즌별 매칭률</p>
                ${seasonBars}
            </div>

            <!-- Effect -->
            <div class="analysis-block" style="border-left-color:${gc};margin-bottom:0.8rem;">
                <strong>착용 시 예상 효과</strong>${result.effect_on_user || ""}
            </div>

            <!-- Styling Tip -->
            <div class="analysis-block" style="border-left-color:var(--primary);">
                <strong>코디 제안</strong>${result.styling_tip || ""}
            </div>

            <!-- Verdict -->
            <div style="margin-top:0.8rem;padding:0.7rem;background:${gc}10;border-radius:8px;text-align:center;font-weight:700;font-size:0.9rem;color:${gc};">
                ${result.verdict || ""}
            </div>
        </div>
    </div>`;
}

// ── Loading Quiz (로딩 중 퀴즈 2~3문제 연속) ──
const LOADING_QUIZ = [
    { celebrity: "수지", hint: "국민 첫사랑 배우 겸 가수", answer: "spring_warm", detail: "봄 웜톤 - 코랄, 피치 계열이 잘 어울려요" },
    { celebrity: "김태희", hint: "대한민국 대표 미인 배우", answer: "summer_cool", detail: "여름 쿨톤 - 라벤더, 로즈 계열이 잘 어울려요" },
    { celebrity: "전지현", hint: "'별에서 온 그대' 주연 배우", answer: "winter_cool", detail: "겨울 쿨톤 - 레드, 블랙, 화이트가 잘 어울려요" },
    { celebrity: "아이유", hint: "국민 여동생, 가수 겸 배우", answer: "spring_warm", detail: "봄 웜톤 - 피치, 코랄 계열이 피부를 밝혀요" },
    { celebrity: "화사", hint: "마마무 멤버, 파격 무대", answer: "autumn_warm", detail: "가을 웜톤 - 테라코타, 브릭 레드가 매력적" },
    { celebrity: "지수", hint: "블랙핑크 멤버 겸 배우", answer: "winter_cool", detail: "겨울 쿨톤 - 비비드 레드, 버건디가 잘 어울려요" },
    { celebrity: "송혜교", hint: "'더 글로리' 주연 배우", answer: "summer_cool", detail: "여름 쿨톤 - 로즈, 파스텔 핑크가 우아해요" },
    { celebrity: "김연아", hint: "피겨 여왕, 국민 영웅", answer: "winter_cool", detail: "겨울 쿨톤 - 화이트, 블랙 대비가 세련돼요" },
    { celebrity: "제니", hint: "블랙핑크 멤버, 솔로 아티스트", answer: "spring_warm", detail: "봄 웜톤 - 화사한 코랄, 오렌지가 잘 어울려요" },
    { celebrity: "윤아", hint: "소녀시대 멤버, CF 퀸", answer: "spring_warm", detail: "봄 웜톤 - 밝은 피치, 살몬 핑크가 생기를 더해요" },
    { celebrity: "아이린", hint: "레드벨벳 리더, 빙의 미모", answer: "summer_cool", detail: "여름 쿨톤 - 소프트 핑크, 라벤더가 청순해요" },
    { celebrity: "이영애", hint: "'대장금' 주연, 한류 원조", answer: "winter_cool", detail: "겨울 쿨톤 - 버건디, 네이비가 기품 있어요" },
];

let _lqQuestions = [];
let _lqIndex = 0;
let _lqScore = 0;

function showLoadingQuiz() {
    const el = $("#loading-quiz-content");
    if (!el) return;

    // 3문제 랜덤 선택 (중복 없이)
    const shuffled = [...LOADING_QUIZ].sort(() => Math.random() - 0.5);
    _lqQuestions = shuffled.slice(0, 3);
    _lqIndex = 0;
    _lqScore = 0;

    renderLoadingQuizQuestion(el);
}

function renderLoadingQuizQuestion(el) {
    if (_lqIndex >= _lqQuestions.length) {
        el.innerHTML = `<div style="text-align:center;padding:0.5rem;">
            <div style="font-size:1.2rem;margin-bottom:0.3rem;">${_lqScore >= 2 ? '🎉' : '💪'}</div>
            <div style="font-size:0.9rem;font-weight:700;">${_lqScore} / ${_lqQuestions.length} 정답!</div>
            <div style="font-size:0.8rem;color:var(--text-sub);margin-top:0.2rem;">${_lqScore >= 2 ? '퍼스널컬러 감각이 있으시네요!' : '분석 결과로 더 알아보세요!'}</div>
        </div>`;
        return;
    }

    const q = _lqQuestions[_lqIndex];
    const options = [
        { key: "spring_warm", ...SM.spring_warm },
        { key: "summer_cool", ...SM.summer_cool },
        { key: "autumn_warm", ...SM.autumn_warm },
        { key: "winter_cool", ...SM.winter_cool },
    ];

    el.innerHTML = `
        <div style="text-align:center;">
            <div style="font-size:0.72rem;color:var(--text-sub);margin-bottom:0.4rem;">${_lqIndex + 1} / ${_lqQuestions.length}</div>
            <p style="font-size:1.1rem;font-weight:700;margin-bottom:0.2rem;">${q.celebrity}</p>
            <p style="font-size:0.78rem;color:var(--text-sub);margin-bottom:0.6rem;">${q.hint}</p>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.4rem;max-width:300px;margin:0 auto;">
                ${options.map(o => `<button class="lq-opt" data-key="${o.key}" style="padding:0.45rem;border:2px solid var(--border);border-radius:10px;background:white;cursor:pointer;font-family:inherit;font-size:0.8rem;font-weight:600;transition:all 0.2s;">${o.emoji} ${o.ko}</button>`).join("")}
            </div>
            <div id="lq-feedback" style="margin-top:0.4rem;min-height:30px;"></div>
        </div>`;

    el.querySelectorAll(".lq-opt").forEach(btn => {
        btn.addEventListener("click", () => {
            const correct = btn.dataset.key === q.answer;
            if (correct) _lqScore++;

            el.querySelectorAll(".lq-opt").forEach(b => {
                b.style.pointerEvents = "none";
                if (b.dataset.key === q.answer) { b.style.borderColor = "#4CAF50"; b.style.background = "#F0FFF0"; }
                else if (b === btn && !correct) { b.style.borderColor = "#EF5350"; b.style.background = "#FFF0F0"; }
            });

            const fb = el.querySelector("#lq-feedback");
            fb.innerHTML = `<div style="font-size:0.78rem;color:${correct ? '#4CAF50' : '#EF5350'};font-weight:600;">${correct ? '정답!' : '아쉽!'} ${q.detail}</div>`;

            setTimeout(() => {
                _lqIndex++;
                renderLoadingQuizQuestion(el);
            }, 1800);
        });
    });
}

// ─── Full Report Download ───
async function downloadReport() {
    const btn = $("#download-report-btn");
    btn.disabled = true;
    btn.textContent = "리포트 생성 중...";

    const r = analysisResult;
    const s = SM[r.season_type] || SM.spring_warm;
    const conf = Math.round((r.confidence || 0) * 100);
    const f = r.face_analysis || {};
    const d = r.draping_simulation || {};
    const st = r.styling || {};
    const best = r.best_colors || [];
    const worst = r.worst_colors || [];
    const detail = r.season_detail || s.ko;
    const faceImg = uploadedImageDataUrl || "";

    // Build one-page report HTML
    const goodC = d.good_colors || [];
    const badC = d.bad_colors || [];
    const ut = r.undertone || "";
    const shortUt = ut.includes("(") ? ut.split("(")[0].trim() : ut;

    // 얼굴+컬러 배경 드레이핑 카드 생성
    const drapeFace = (colors, label, borderColor) => colors.slice(0, 4).map(c => `
        <div style="text-align:center;">
            <div style="width:90px;height:110px;background:${c.hex};border-radius:10px;display:flex;align-items:flex-end;justify-content:center;overflow:hidden;border:2px solid ${borderColor};">
                ${faceImg ? `<img src="${faceImg}" style="width:80px;height:80px;object-fit:cover;border-radius:50%;margin-bottom:6px;border:2px solid white;">` : ""}
            </div>
            <div style="font-size:9px;font-weight:700;margin-top:4px;color:#2D2D2D;">${c.color}</div>
            <div style="font-size:7.5px;color:#6B6B6B;line-height:1.3;max-width:90px;margin-top:2px;">${c.effect}</div>
        </div>`).join("");

    // 큰 컬러바 + 설명
    const colorBar = (colors, label, labelColor) => colors.map(c => `
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
            <div style="width:80px;height:22px;border-radius:6px;background:${c.hex};border:1px solid #e0e0e0;flex-shrink:0;"></div>
            <div style="font-size:8px;color:#2D2D2D;line-height:1.4;"><b>${c.color}</b> ${c.reason || ""}</div>
        </div>`).join("");

    const report = $("#full-report");
    report.classList.remove("hidden");
    report.innerHTML = `
    <div class="report-page" id="report-capture">
        <!-- Header -->
        <div style="text-align:center;padding:20px 24px 12px;border-bottom:2px solid ${s.accent};">
            <div style="font-size:18px;font-weight:800;color:#2D2D2D;">퍼스널 컬러 & 얼굴 인상 분석 리포트</div>
        </div>

        <!-- Type Info -->
        <div style="padding:12px 24px;display:flex;gap:12px;">
            <div style="flex:1;background:#F8F8F8;border-radius:8px;padding:8px 12px;">
                <div style="font-size:8px;color:#999;">한 줄 요약</div>
                <div style="font-size:11px;font-weight:700;color:#2D2D2D;margin-top:2px;"><b>${shortUt}</b>. ${r.undertone_reason || ""}</div>
            </div>
            <div style="flex:1;background:#F8F8F8;border-radius:8px;padding:8px 12px;">
                <div style="font-size:8px;color:#999;">세부 타입</div>
                <div style="font-size:14px;font-weight:800;color:${s.accent};margin-top:2px;">${detail}</div>
                <div style="font-size:8px;color:#999;">${s.vibe}</div>
            </div>
        </div>

        <!-- Visual Draping Comparison -->
        <div style="padding:10px 24px;">
            <div style="text-align:center;font-size:12px;font-weight:700;margin-bottom:10px;color:#2D2D2D;">비주얼 비교 영역</div>
            <div style="display:flex;justify-content:center;gap:8px;">
                <!-- Best 4 -->
                <div>
                    <div style="text-align:center;font-size:9px;font-weight:700;color:#4CAF50;margin-bottom:6px;padding:3px 10px;background:#F0FFF0;border-radius:4px;border:1px solid #4CAF50;">잘 어울리는 컬러 (BEST 4)</div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;">
                        ${drapeFace(goodC, "BEST", "#4CAF50")}
                    </div>
                </div>
                <!-- Face Center -->
                <div style="display:flex;align-items:center;">
                    ${faceImg ? `<img src="${faceImg}" style="width:100px;height:120px;object-fit:cover;border-radius:12px;border:3px solid #E8E8E8;">` : ""}
                </div>
                <!-- Worst 4 -->
                <div>
                    <div style="text-align:center;font-size:9px;font-weight:700;color:#EF5350;margin-bottom:6px;padding:3px 10px;background:#FFF0F0;border-radius:4px;border:1px solid #EF5350;">안 어울리는 컬러 (WORST 4)</div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;">
                        ${drapeFace(badC, "WORST", "#EF5350")}
                    </div>
                </div>
            </div>
        </div>

        <!-- Face Analysis + Strengths -->
        <div style="padding:8px 24px;">
            <div style="text-align:center;font-size:12px;font-weight:700;padding-bottom:4px;border-bottom:1px solid #ddd;margin-bottom:8px;">얼굴 분석</div>
            <div style="display:flex;gap:10px;">
                <!-- Face Details -->
                <div style="flex:1;background:#F8F8F8;border-radius:8px;padding:8px;font-size:8px;line-height:1.8;">
                    <b>피부</b> · ${f.skin || ""}<br>
                    <b>눈동자</b> · ${f.eyes || ""}<br>
                    <b>머리색</b> · ${f.hair || ""}<br>
                    <b>대비감</b> · ${f.face_contrast || ""}
                </div>
                <!-- Strengths -->
                <div style="flex:1;">
                    <div style="background:#F0FFF0;border-radius:8px;padding:8px;margin-bottom:4px;">
                        <div style="font-size:8px;font-weight:700;color:#4CAF50;margin-bottom:3px;">장점 분석</div>
                        ${(f.strengths || []).map(x => `<div style="font-size:7.5px;line-height:1.6;">• ${x}</div>`).join("")}
                    </div>
                    <div style="background:#FFF8F0;border-radius:8px;padding:8px;">
                        <div style="font-size:8px;font-weight:700;color:#FF9800;margin-bottom:3px;">보완 포인트</div>
                        ${(f.improvements || []).map(x => `<div style="font-size:7.5px;line-height:1.6;">• ${x}</div>`).join("")}
                    </div>
                </div>
            </div>
        </div>

        <!-- Best/Worst Colors with large bars -->
        <div style="padding:8px 24px;">
            <div style="display:flex;gap:16px;">
                <div style="flex:1;">
                    <div style="font-size:10px;font-weight:700;color:#4CAF50;margin-bottom:6px;">[추천 컬러] BEST 5</div>
                    ${colorBar(best, "BEST", "#4CAF50")}
                </div>
                <div style="flex:1;">
                    <div style="font-size:10px;font-weight:700;color:#EF5350;margin-bottom:6px;">[피해야 할 컬러] WORST</div>
                    ${colorBar(worst, "WORST", "#EF5350")}
                </div>
            </div>
        </div>

        <!-- Styling with color circles -->
        <div style="padding:8px 24px;">
            <div style="display:flex;gap:10px;">
                <div style="flex:1;background:#F8F8F8;border-radius:8px;padding:8px;">
                    <div style="font-size:9px;font-weight:700;margin-bottom:4px;">메이크업</div>
                    <div style="font-size:7.5px;line-height:1.7;">
                        <b>립</b> ${st.makeup_lip || ""}<br>
                        <b>블러셔</b> ${st.makeup_blush || ""}<br>
                        <b>섀도우</b> ${st.makeup_eyeshadow || ""}
                    </div>
                </div>
                <div style="flex:1;background:#F8F8F8;border-radius:8px;padding:8px;">
                    <div style="font-size:9px;font-weight:700;margin-bottom:4px;">헤어 & 패션</div>
                    <div style="font-size:7.5px;line-height:1.7;">
                        <b>추천 헤어</b> ${st.hair_recommended || ""}<br>
                        <b>피해야 할 헤어</b> ${st.hair_avoid || ""}<br>
                        <b>패션 조합</b> ${st.fashion_combinations || ""}
                    </div>
                </div>
            </div>
        </div>

        <!-- Conclusion -->
        <div style="margin:8px 24px;padding:10px;background:${s.accent}15;border-radius:10px;border:1px solid ${s.accent}40;text-align:center;">
            <div style="font-size:11px;font-weight:700;color:#2D2D2D;">${r.one_line_conclusion || ""}</div>
        </div>

        <div style="display:flex;justify-content:space-between;padding:8px 24px;font-size:7px;color:#ccc;border-top:1px solid #eee;margin-top:4px;">
            <span>Beauty AI Analyze</span>
            <span>beauty-ai-analyze.onrender.com</span>
        </div>
    </div>`;

    // Capture with html2canvas
    try {
        await new Promise(r => setTimeout(r, 300)); // wait for images
        const canvas = await html2canvas(document.getElementById("report-capture"), {
            scale: 2,
            useCORS: true,
            allowTaint: true,
            backgroundColor: "#FFFFFF",
            width: 800,
            windowWidth: 800,
        });
        const link = document.createElement("a");
        link.download = "personal_color_report.png";
        link.href = canvas.toDataURL("image/png");
        link.click();
        gEvent("report_download", { season_type: r.season_type });
    } catch (e) {
        alert("리포트 생성 중 오류가 발생했습니다: " + e.message);
    } finally {
        report.classList.add("hidden");
        btn.disabled = false;
        btn.textContent = "전체 리포트 다운로드 (이미지)";
    }
}
