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
    if (analyzeBtn) analyzeBtn.addEventListener("click", runAnalysis);
    if (resetBtn) resetBtn.addEventListener("click", resetAll);
    if (dlBtn) dlBtn.addEventListener("click", downloadReport);
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
    spring_warm: { emoji: "🌸", ko: "봄 웜톤", en: "Spring Warm", cls: "spring", accent: "#FF8FAB" },
    summer_cool: { emoji: "🌊", ko: "여름 쿨톤", en: "Summer Cool", cls: "summer", accent: "#C8A2C8" },
    autumn_warm: { emoji: "🍂", ko: "가을 웜톤", en: "Autumn Warm", cls: "autumn", accent: "#CD853F" },
    winter_cool: { emoji: "❄️", ko: "겨울 쿨톤", en: "Winter Cool", cls: "winter", accent: "#DC143C" },
};
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

    $("#result-header").innerHTML = `
        <div class="result-header-with-face">
            ${faceImg}
            <div class="result-header-info">
                <div class="result-header-inner">
                    <span class="season-badge season-${s.cls}">${s.emoji} ${detail}</span>
                    <span style="color:var(--text-sub);font-size:0.85rem;">${s.en}</span>
                </div>
                <div style="margin-top:1rem;">
                    <div style="display:flex;justify-content:space-between;font-size:0.85rem;">
                        <span style="font-weight:600;">분석 확신도</span>
                        <span style="color:var(--text-sub);">${conf}%</span>
                    </div>
                    <div class="conf-bar"><div class="conf-fill ${confCls}" style="width:${conf}%"></div></div>
                </div>
                ${conclusion ? `<div class="conclusion-box"><strong>한 줄 결론</strong> ${conclusion}</div>` : ""}
            </div>
        </div>`;

    $("#results-section").classList.remove("hidden");
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
    }
}

// ── Draping ──
function renderDraping(r) {
    const d = r.draping_simulation || {};
    const mapColor = (arr, good) => (arr || []).map((c) => `
        <div class="draping-item">
            <div class="color-chip" style="background:${c.hex}"></div>
            <div class="info"><div class="color-name">${c.color}</div><div class="effect">${c.effect}</div></div>
        </div>`).join("");

    const best = r.best_colors || [], worst = r.worst_colors || [];
    let colorsHtml = "";
    if (best.length && typeof best[0] === "object") {
        colorsHtml = `<div class="card" style="margin-top:1rem;">
            <h3 class="section-title">추천 & 비추천 컬러</h3>
            <div class="colors-grid">
                <div><p style="font-weight:700;color:var(--green);margin-bottom:0.8rem;">BEST 컬러</p>
                    ${best.map((c) => `<div class="color-item"><div class="chip" style="background:${c.hex}"></div><span class="name">${c.color}</span><span class="reason">${c.reason}</span></div>`).join("")}
                </div>
                <div><p style="font-weight:700;color:var(--red);margin-bottom:0.8rem;">WORST 컬러</p>
                    ${worst.map((c) => `<div class="color-item"><div class="chip" style="background:${c.hex}"></div><span class="name">${c.color}</span><span class="reason">${c.reason}</span></div>`).join("")}
                </div>
            </div></div>`;
    }
    return `<div class="card">
        <h3 class="section-title">컬러 드레이핑 시뮬레이션</h3>
        <p class="section-sub">실제 드레이핑을 했을 때 얼굴에 나타나는 변화를 분석했습니다.</p>
        <div class="draping-grid">
            <div><p style="font-weight:700;color:var(--green);margin-bottom:1rem;">잘 어울리는 컬러</p>${mapColor(d.good_colors)}</div>
            <div><p style="font-weight:700;color:var(--red);margin-bottom:1rem;">안 어울리는 컬러</p>${mapColor(d.bad_colors)}</div>
        </div></div>${colorsHtml}`;
}

// ── Face ──
function renderFace(r) {
    const f = r.face_analysis || {};
    const faceImg = uploadedImageDataUrl ? `<div style="text-align:center;margin-bottom:1.5rem;"><img src="${uploadedImageDataUrl}" style="width:180px;height:180px;object-fit:cover;border-radius:50%;border:4px solid var(--border);" alt=""></div>` : "";
    return `<div class="card">
        <h3 class="section-title">얼굴 인상 분석</h3>
        ${faceImg}
        <div class="face-grid">
            <div class="analysis-block" style="border-left-color:#FFB6C1"><strong>피부</strong>${hexToChip(f.skin)}</div>
            <div class="analysis-block" style="border-left-color:#87CEEB"><strong>눈동자</strong>${hexToChip(f.eyes)}</div>
            <div class="analysis-block" style="border-left-color:#DEB887"><strong>머리카락</strong>${hexToChip(f.hair)}</div>
            <div class="analysis-block" style="border-left-color:#C0C0C0"><strong>대비감</strong>${hexToChip(f.face_contrast)}</div>
        </div>
        <div class="face-grid">
            <div class="strength-box"><h4>나의 강점</h4><ul>${(f.strengths || []).map((s) => `<li>${s}</li>`).join("") || "<li>-</li>"}</ul></div>
            <div class="improve-box"><h4>보완 포인트</h4><ul>${(f.improvements || []).map((s) => `<li>${s}</li>`).join("") || "<li>-</li>"}</ul></div>
        </div></div>`;
}

// ── Palette ──
async function renderPalette(el, r) {
    el.innerHTML = `<div class="card"><div class="loading-content"><div class="spinner"></div></div></div>`;
    try {
        const resp = await fetch(`/api/palettes/${r.season_type}`);
        const data = await resp.json();
        const s = SM[r.season_type];
        const sw = (arr) => (arr || []).map((c) => `<div class="swatch"><div class="swatch-color" style="background:${c.hex}" title="${c.name}"></div><div class="swatch-name">${c.name}</div></div>`).join("");
        el.innerHTML = `<div class="card">
            <h3 class="section-title">${s.emoji} ${data.name || s.ko} 컬러 팔레트</h3>
            <p style="font-weight:700;color:var(--green);margin-bottom:0.8rem;">Best Colors</p>
            <div class="palette-wrap">${sw(data.best)}</div>
            <hr style="border:none;border-top:1px solid var(--border);margin:1.5rem 0;">
            <p style="font-weight:700;color:var(--red);margin-bottom:0.8rem;">Worst Colors</p>
            <div class="palette-wrap">${sw(data.worst)}</div></div>`;
    } catch { el.innerHTML = `<div class="card"><p>팔레트를 불러올 수 없습니다.</p></div>`; }
}

// ── Styling ──
function renderStyling(r) {
    const st = r.styling || {}, s = SM[r.season_type] || {};
    return `<div class="card">
        <h3 class="section-title">스타일링 제안</h3>
        <p style="font-weight:700;margin-bottom:0.8rem;">메이크업</p>
        <div class="styling-makeup-grid">
            <div class="analysis-block" style="border-left-color:#E8A0BF"><strong>립</strong>${hexToChip(st.makeup_lip)}</div>
            <div class="analysis-block" style="border-left-color:#FFB6C1"><strong>블러셔</strong>${hexToChip(st.makeup_blush)}</div>
            <div class="analysis-block" style="border-left-color:#DDA0DD"><strong>아이섀도</strong>${hexToChip(st.makeup_eyeshadow)}</div>
        </div>
        <p style="font-weight:700;margin-bottom:0.8rem;">헤어컬러</p>
        <div class="hair-grid">
            <div class="hair-good"><p>추천</p><p style="font-size:0.88rem;line-height:1.6">${hexToChip(st.hair_recommended)}</p></div>
            <div class="hair-bad"><p>피하기</p><p style="font-size:0.88rem;line-height:1.6">${hexToChip(st.hair_avoid)}</p></div>
        </div>
        <p style="font-weight:700;margin-bottom:0.8rem;">패션 색 조합</p>
        <div class="analysis-block" style="border-left-color:${s.accent || "var(--primary)"}">${hexToChip(st.fashion_combinations)}</div>
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
    const buyBtn = buyUrl ? `<a href="${buyUrl}" target="_blank" rel="noopener" class="buy-link" onclick="gEvent('product_click',{brand:'${brand}',product:'${item.name.replace(/'/g,"")}'})">구매하기 →</a>` : "";

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
    const report = $("#full-report");
    report.classList.remove("hidden");
    report.innerHTML = `
    <div class="report-page" id="report-capture">
        <!-- Header -->
        <div class="rpt-header" style="background:linear-gradient(135deg,${s.accent}cc,${s.accent}66);">
            <div class="rpt-header-top">
                <div class="rpt-badge">Personal Color & Face Analysis Report</div>
                <div class="rpt-conf">확신도 ${conf}%</div>
            </div>
            <div class="rpt-header-main">
                ${faceImg ? `<img src="${faceImg}" class="rpt-face">` : ""}
                <div>
                    <div class="rpt-season">${s.emoji} ${detail}</div>
                    <div class="rpt-season-en">${s.en}</div>
                    ${r.one_line_conclusion ? `<div class="rpt-conclusion">${r.one_line_conclusion}</div>` : ""}
                </div>
            </div>
        </div>

        <!-- Face Analysis -->
        <div class="rpt-section">
            <div class="rpt-title">얼굴 인상 분석</div>
            <div class="rpt-2col">
                <div class="rpt-block"><strong>피부</strong> ${f.skin || ""}</div>
                <div class="rpt-block"><strong>눈동자</strong> ${f.eyes || ""}</div>
                <div class="rpt-block"><strong>머리카락</strong> ${f.hair || ""}</div>
                <div class="rpt-block"><strong>대비감</strong> ${f.face_contrast || ""}</div>
            </div>
            <div class="rpt-2col">
                <div class="rpt-good">
                    <strong>강점</strong>
                    ${(f.strengths || []).map(s => `<span>• ${s}</span>`).join("")}
                </div>
                <div class="rpt-bad">
                    <strong>보완 포인트</strong>
                    ${(f.improvements || []).map(s => `<span>• ${s}</span>`).join("")}
                </div>
            </div>
        </div>

        <!-- Draping -->
        <div class="rpt-section">
            <div class="rpt-title">컬러 드레이핑</div>
            <div class="rpt-2col">
                <div>
                    <div class="rpt-label" style="color:#4CAF50;">BEST</div>
                    ${(d.good_colors || []).map(c => `<div class="rpt-color-row"><div style="width:24px;height:24px;min-width:24px;border-radius:6px;border:1px solid #ddd;background-color:${c.hex};"></div><span><b>${c.color}</b> ${c.effect}</span></div>`).join("")}
                </div>
                <div>
                    <div class="rpt-label" style="color:#EF5350;">WORST</div>
                    ${(d.bad_colors || []).map(c => `<div class="rpt-color-row"><div style="width:24px;height:24px;min-width:24px;border-radius:6px;border:1px solid #ddd;background-color:${c.hex};"></div><span><b>${c.color}</b> ${c.effect}</span></div>`).join("")}
                </div>
            </div>
        </div>

        <!-- Best/Worst Colors -->
        <div class="rpt-section">
            <div class="rpt-title">추천 컬러</div>
            <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:8px;">
                ${best.map(c => `<div style="text-align:center;"><div style="width:40px;height:40px;border-radius:8px;border:1px solid #ddd;background-color:${c.hex};"></div><div style="font-size:9px;color:#6B6B6B;margin-top:3px;">${c.color}</div></div>`).join("")}
            </div>
            <div class="rpt-title" style="margin-top:0.8rem;">피해야 할 컬러</div>
            <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:8px;">
                ${worst.map(c => `<div style="text-align:center;"><div style="width:40px;height:40px;border-radius:8px;border:1px solid #ddd;background-color:${c.hex};"></div><div style="font-size:9px;color:#6B6B6B;margin-top:3px;">${c.color}</div></div>`).join("")}
            </div>
        </div>

        <!-- Styling -->
        <div class="rpt-section">
            <div class="rpt-title">스타일링 제안</div>
            <div class="rpt-3col">
                <div class="rpt-block"><strong>립</strong> ${st.makeup_lip || ""}</div>
                <div class="rpt-block"><strong>블러셔</strong> ${st.makeup_blush || ""}</div>
                <div class="rpt-block"><strong>아이섀도</strong> ${st.makeup_eyeshadow || ""}</div>
            </div>
            <div class="rpt-2col" style="margin-top:0.5rem;">
                <div class="rpt-block"><strong>추천 헤어</strong> ${st.hair_recommended || ""}</div>
                <div class="rpt-block"><strong>패션 조합</strong> ${st.fashion_combinations || ""}</div>
            </div>
        </div>

        <div class="rpt-footer">
            <span>Beauty AI Analyze</span>
            <span>ai-beauty-analyze.streamlit.app</span>
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
