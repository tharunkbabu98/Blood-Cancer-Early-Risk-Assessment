import streamlit as st
import pandas as pd
from risk_engine import RiskAssessmentEngine

st.set_page_config(
    page_title="BloodScan AI · Risk Assessment",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@300;400;500;600;700&family=Share+Tech+Mono&display=swap');

:root {
    --red:        #ff2442;
    --red-dim:    rgba(255,36,66,0.15);
    --red-mid:    rgba(255,36,66,0.35);
    --red-glow:   0 0 20px rgba(255,36,66,0.5), 0 0 60px rgba(255,36,66,0.15);
    --amber:      #ffaa00;
    --green:      #00ffaa;
    --bg:         #03050a;
    --surface:    rgba(255,255,255,0.025);
    --border:     rgba(255,36,66,0.18);
    --text:       #c8d8f0;
    --text-dim:   #5a6a80;
    --mono:       'Share Tech Mono', monospace;
    --display:    'Orbitron', sans-serif;
    --body:       'Rajdhani', sans-serif;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--body) !important;
    font-size: 16px;
}

/* ── Animated background ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 70% 60% at 15% 0%,   rgba(255,36,66,0.10) 0%, transparent 55%),
        radial-gradient(ellipse 50% 40% at 85% 100%,  rgba(255,36,66,0.07) 0%, transparent 55%),
        radial-gradient(ellipse 40% 30% at 50% 50%,   rgba(0,80,200,0.05) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
    animation: bgPulse 8s ease-in-out infinite alternate;
}
@keyframes bgPulse {
    0%   { opacity: 0.7; }
    100% { opacity: 1.0; }
}

/* ── Scanline overlay ── */
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,0,0,0.06) 2px,
        rgba(0,0,0,0.06) 4px
    );
    pointer-events: none;
    z-index: 1;
}

[data-testid="stHeader"]  { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }
section[data-testid="stMain"] > div { padding-top: 0 !important; }
.block-container {
    padding: 0 2.5rem 5rem !important;
    max-width: 1120px !important;
    margin: 0 auto;
    position: relative;
    z-index: 2;
}

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 4rem 2rem 2.5rem;
    position: relative;
}
.hero-eyebrow {
    font-family: var(--mono);
    font-size: 0.68rem;
    letter-spacing: 0.3em;
    color: var(--red);
    text-transform: uppercase;
    margin-bottom: 1rem;
    animation: fadeDown 0.6s ease both;
}
.hero-eyebrow::before { content: '[ '; }
.hero-eyebrow::after  { content: ' ]'; }

.hero h1 {
    font-family: var(--display) !important;
    font-size: clamp(2.2rem, 6vw, 4rem) !important;
    font-weight: 900 !important;
    color: #fff !important;
    letter-spacing: 0.08em !important;
    line-height: 1 !important;
    margin-bottom: 0.5rem !important;
    text-shadow: var(--red-glow) !important;
    animation: fadeDown 0.7s 0.1s ease both !important;
}
.hero h1 .accent { color: var(--red); }
.hero h1 .sub {
    font-size: 0.4em;
    font-weight: 400;
    letter-spacing: 0.25em;
    color: var(--text-dim);
    display: block;
    margin-top: 0.4em;
}

.hero-desc {
    font-family: var(--body);
    font-size: 1rem;
    font-weight: 300;
    color: var(--text-dim);
    max-width: 480px;
    margin: 1.2rem auto 0;
    line-height: 1.7;
    letter-spacing: 0.02em;
    animation: fadeDown 0.8s 0.2s ease both;
}

/* Corner decorations */
.hero-corners {
    position: relative;
    display: inline-block;
    padding: 1.5rem 3rem;
    margin-bottom: 0.5rem;
}
.hero-corners::before,
.hero-corners::after,
.corner-bl::before,
.corner-bl::after {
    content: '';
    position: absolute;
    width: 18px; height: 18px;
    border-color: var(--red);
    border-style: solid;
    opacity: 0.6;
}
.hero-corners::before { top: 0; left: 0; border-width: 2px 0 0 2px; }
.hero-corners::after  { top: 0; right: 0; border-width: 2px 2px 0 0; }
.corner-bl::before    { bottom: 0; left: 0; border-width: 0 0 2px 2px; }
.corner-bl::after     { bottom: 0; right: 0; border-width: 0 2px 2px 0; }

.hero-line {
    width: 1px;
    height: 40px;
    background: linear-gradient(to bottom, var(--red), transparent);
    margin: 1.5rem auto 0;
    animation: fadeDown 1s 0.3s ease both;
}

@keyframes fadeDown {
    from { opacity: 0; transform: translateY(-12px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Section Cards ── */
.card {
    position: relative;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1.8rem 2rem;
    margin-bottom: 1rem;
    overflow: hidden;
    transition: border-color 0.3s, box-shadow 0.3s;
}
.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--red), transparent);
    opacity: 0.6;
}
.card:hover {
    border-color: rgba(255,36,66,0.4);
    box-shadow: 0 0 30px rgba(255,36,66,0.08), inset 0 0 30px rgba(255,36,66,0.02);
}

/* Corner accents on cards */
.card::after {
    content: '';
    position: absolute;
    bottom: 0; right: 0;
    width: 12px; height: 12px;
    border-right: 1px solid var(--red);
    border-bottom: 1px solid var(--red);
    opacity: 0.5;
}

.card-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 1.5rem;
}
.card-header-num {
    font-family: var(--mono);
    font-size: 0.62rem;
    color: var(--red);
    opacity: 0.7;
    min-width: 24px;
}
.card-header-title {
    font-family: var(--display);
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--red);
}
.card-header-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--red-mid), transparent);
}
.card-header-tag {
    font-family: var(--mono);
    font-size: 0.58rem;
    color: var(--text-dim);
    letter-spacing: 0.1em;
}

/* ── Inputs ── */
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,36,66,0.04) !important;
    border: 1px solid rgba(255,36,66,0.2) !important;
    border-radius: 3px !important;
    color: #e8f0ff !important;
    font-family: var(--mono) !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: var(--red) !important;
    box-shadow: 0 0 0 2px rgba(255,36,66,0.15), var(--red-glow) !important;
    background: rgba(255,36,66,0.07) !important;
}

label, [data-testid="stWidgetLabel"] p {
    font-family: var(--mono) !important;
    font-size: 0.72rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.1em !important;
    color: #6a7a94 !important;
    text-transform: uppercase !important;
}

/* ── Sliders ── */
[data-testid="stSlider"] > div > div > div {
    background: rgba(255,36,66,0.15) !important;
    height: 3px !important;
}
[data-testid="stSlider"] > div > div > div > div {
    background: var(--red) !important;
    box-shadow: 0 0 10px rgba(255,36,66,0.6) !important;
    border-radius: 2px !important;
    transition: background 0.3s, box-shadow 0.3s !important;
}

/* ── CTA Button ── */
.stButton > button {
    width: 100% !important;
    position: relative !important;
    background: transparent !important;
    border: 1px solid var(--red) !important;
    border-radius: 3px !important;
    color: #fff !important;
    font-family: var(--display) !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.25em !important;
    text-transform: uppercase !important;
    padding: 1.1rem 2rem !important;
    cursor: pointer !important;
    overflow: hidden !important;
    transition: all 0.3s !important;
    box-shadow: inset 0 0 20px rgba(255,36,66,0.05), var(--red-glow) !important;
}
.stButton > button::before {
    content: '' !important;
    position: absolute !important;
    inset: 0 !important;
    background: linear-gradient(135deg, rgba(255,36,66,0.15), transparent 60%) !important;
    transition: opacity 0.3s !important;
}
.stButton > button:hover {
    background: rgba(255,36,66,0.12) !important;
    box-shadow: 0 0 40px rgba(255,36,66,0.4), inset 0 0 30px rgba(255,36,66,0.1) !important;
    transform: translateY(-1px) !important;
    letter-spacing: 0.3em !important;
}

/* ── Result ── */
.result-wrap {
    position: relative;
    border-radius: 4px;
    padding: 2.5rem 2rem;
    margin: 1.5rem 0;
    text-align: center;
    overflow: hidden;
}
.result-wrap.low {
    background: linear-gradient(135deg, rgba(0,255,170,0.08), rgba(0,255,170,0.02));
    border: 1px solid rgba(0,255,170,0.3);
    box-shadow: 0 0 40px rgba(0,255,170,0.07);
}
.result-wrap.moderate {
    background: linear-gradient(135deg, rgba(255,170,0,0.1), rgba(255,170,0,0.02));
    border: 1px solid rgba(255,170,0,0.35);
    box-shadow: 0 0 40px rgba(255,170,0,0.08);
}
.result-wrap.high {
    background: linear-gradient(135deg, rgba(255,36,66,0.12), rgba(255,36,66,0.02));
    border: 1px solid rgba(255,36,66,0.45);
    box-shadow: 0 0 60px rgba(255,36,66,0.12);
}

.result-tag {
    font-family: var(--mono);
    font-size: 0.62rem;
    letter-spacing: 0.3em;
    color: var(--text-dim);
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.result-level {
    font-family: var(--display);
    font-size: clamp(2.5rem, 6vw, 4.5rem);
    font-weight: 900;
    letter-spacing: 0.1em;
    line-height: 1;
    margin-bottom: 0.8rem;
}
.result-level.low      { color: var(--green); text-shadow: 0 0 30px rgba(0,255,170,0.6); }
.result-level.moderate { color: var(--amber); text-shadow: 0 0 30px rgba(255,170,0,0.6); }
.result-level.high     { color: var(--red);   text-shadow: var(--red-glow); }

.urgency-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 2px;
    padding: 0.4rem 1rem;
    font-family: var(--mono);
    font-size: 0.72rem;
    letter-spacing: 0.15em;
    color: var(--text-dim);
}
.urgency-dot {
    width: 5px; height: 5px;
    border-radius: 50%;
    background: var(--red);
    box-shadow: 0 0 8px var(--red);
    animation: blink 1.2s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }

/* ── Abnormality items ── */
.ab-item {
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
    background: rgba(255,36,66,0.05);
    border-left: 2px solid var(--red);
    border-bottom: 1px solid rgba(255,36,66,0.1);
    padding: 0.7rem 1rem;
    margin-bottom: 0.4rem;
    font-family: var(--body);
    font-size: 0.9rem;
    font-weight: 400;
    color: #ffb0bb;
    letter-spacing: 0.02em;
    transition: background 0.2s;
}
.ab-item:hover { background: rgba(255,36,66,0.09); }
.ab-num {
    font-family: var(--mono);
    font-size: 0.6rem;
    color: var(--red);
    opacity: 0.6;
    padding-top: 3px;
    min-width: 20px;
}

/* ── Recommendation ── */
.rec-box {
    background: rgba(0,255,170,0.04);
    border: 1px solid rgba(0,255,170,0.2);
    border-left: 3px solid var(--green);
    border-radius: 3px;
    padding: 1.2rem 1.4rem;
    font-family: var(--body);
    font-size: 0.95rem;
    font-weight: 400;
    color: #90ffd8;
    line-height: 1.7;
    letter-spacing: 0.02em;
}

/* ── Severity badge ── */
.sev-badge {
    font-family: var(--mono);
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    font-weight: 600;
    text-transform: uppercase;
    text-align: right;
    margin: -12px 0 10px;
    transition: color 0.3s;
}

/* ── Status bar at top ── */
.status-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5rem 0;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255,36,66,0.1);
}
.status-item {
    font-family: var(--mono);
    font-size: 0.6rem;
    letter-spacing: 0.12em;
    color: var(--text-dim);
}
.status-item .dot {
    display: inline-block;
    width: 4px; height: 4px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 6px var(--green);
    margin-right: 5px;
    animation: blink 2s ease-in-out infinite;
}

hr { border-color: rgba(255,36,66,0.1) !important; }
[data-testid="stExpander"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Status bar ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="status-bar">
    <span class="status-item"><span class="dot"></span>SYSTEM ONLINE</span>
    <span class="status-item">BLOODSCAN AI · v2.4.1</span>
    <span class="status-item">HEMATOLOGY MODULE · ACTIVE</span>
</div>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Hematological Risk Screening System</div>
    <div class="hero-corners">
        <div class="corner-bl">
            <h1>BLOOD<span class="accent">SCAN</span><span class="sub">EARLY DETECTION · AI POWERED</span></h1>
        </div>
    </div>
    <p class="hero-desc">
        Advanced CBC analysis combined with symptom pattern recognition
        to flag early indicators of hematological malignancies.
    </p>
    <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)

NORMAL_CBC = {
    "Hemoglobin": {"Male": 15.0, "Female": 13.5},
    "WBC": 7.5,
    "Platelets": 275
}

engine = RiskAssessmentEngine()

# ── Patient Details ───────────────────────────────────────────────────────────
st.markdown("""
<div class="card">
<div class="card-header">
    <span class="card-header-num">01</span>
    <span class="card-header-title">Patient Profile</span>
    <span class="card-header-line"></span>
    <span class="card-header-tag">DEMOGRAPHIC DATA</span>
</div>
""", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age [ years ]", 18, 100, 30)
with col2:
    gender = st.selectbox("Biological Sex", ["Male", "Female"])
st.markdown('</div>', unsafe_allow_html=True)

# ── CBC ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="card">
<div class="card-header">
    <span class="card-header-num">02</span>
    <span class="card-header-title">Complete Blood Count</span>
    <span class="card-header-line"></span>
    <span class="card-header-tag">CBC PANEL</span>
</div>
""", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    hemoglobin = st.number_input("Hemoglobin [ g/dL ]", 4.0, 20.0, 13.5)
    wbc        = st.number_input("WBC Count [ ×10³/μL ]", 0.5, 100.0, 7.0)
with col2:
    rbc        = st.number_input("RBC Count [ ×10⁶/μL ]", 1.5, 7.0, 4.5)
    platelets  = st.number_input("Platelet Count [ ×10³/μL ]", 10, 600, 250)
st.markdown('</div>', unsafe_allow_html=True)

# ── Symptoms ──────────────────────────────────────────────────────────────────
symptom_list = [
    ("fatigue",             "Fatigue"),
    ("fever",               "Fever"),
    ("weight_loss",         "Weight Loss"),
    ("night_sweats",        "Night Sweats"),
    ("easy_bruising",       "Easy Bruising"),
    ("frequent_infections", "Frequent Infections"),
    ("lymph_node_swelling", "Lymph Node Swelling"),
    ("bone_pain",           "Bone Pain"),
    ("shortness_of_breath", "Shortness of Breath"),
    ("bleeding_gums",       "Bleeding Gums"),
]

severity_labels = {0: "——", 1: "MILD", 2: "MODERATE", 3: "SEVERE"}
severity_colors = {0: "#2a3545", 1: "#f97316", 2: "#ef4444", 3: "#ff2442"}
severity_glow   = {
    0: "none",
    1: "0 0 8px rgba(249,115,22,0.5)",
    2: "0 0 12px rgba(239,68,68,0.6)",
    3: "0 0 20px rgba(255,36,66,0.9), 0 0 40px rgba(255,36,66,0.3)"
}

st.markdown("""
<div class="card">
<div class="card-header">
    <span class="card-header-num">03</span>
    <span class="card-header-title">Clinical Symptoms</span>
    <span class="card-header-line"></span>
    <span class="card-header-tag">0 = NONE · 3 = SEVERE</span>
</div>
""", unsafe_allow_html=True)

symptoms = {}
half = len(symptom_list) // 2
col1, col2 = st.columns(2)

with col1:
    for key, label in symptom_list[:half]:
        val = st.slider(label.upper(), 0, 3, 0, key=key)
        symptoms[key] = val
        c = severity_colors[val]
        s = severity_labels[val]
        st.markdown(
            f'<div class="sev-badge" style="color:{c};text-shadow:{severity_glow[val]};">{s}</div>',
            unsafe_allow_html=True
        )

with col2:
    for key, label in symptom_list[half:]:
        val = st.slider(label.upper(), 0, 3, 0, key=key)
        symptoms[key] = val
        c = severity_colors[val]
        s = severity_labels[val]
        st.markdown(
            f'<div class="sev-badge" style="color:{c};text-shadow:{severity_glow[val]};">{s}</div>',
            unsafe_allow_html=True
        )

# ── Dynamic slider JS ─────────────────────────────────────────────────────────
st.markdown("""
<script>
(function() {
    const thumbColor = { 0:'#2a3545', 1:'#f97316', 2:'#ef4444', 3:'#ff2442' };
    const thumbGlow  = {
        0:'none',
        1:'0 0 8px rgba(249,115,22,0.6)',
        2:'0 0 14px rgba(239,68,68,0.7)',
        3:'0 0 22px rgba(255,36,66,1), 0 0 40px rgba(255,36,66,0.4)'
    };
    const trackColor = {
        0:'rgba(255,36,66,0.1)',
        1:'rgba(249,115,22,0.4)',
        2:'rgba(239,68,68,0.65)',
        3:'rgba(255,36,66,1)'
    };
    function apply() {
        document.querySelectorAll('[data-testid="stSlider"]').forEach(w => {
            const inp = w.querySelector('input[type="range"]');
            if (!inp) return;
            const v = Math.min(3, Math.max(0, Math.round(parseFloat(inp.value)||0)));
            inp.style.accentColor = thumbColor[v];
            const thumb = w.querySelector('[role="slider"]');
            if (thumb) {
                thumb.style.background  = thumbColor[v];
                thumb.style.boxShadow   = thumbGlow[v];
                thumb.style.transition  = 'background 0.25s, box-shadow 0.25s';
                thumb.style.borderColor = thumbColor[v];
            }
            const fills = w.querySelectorAll('div[data-baseweb] div');
            fills.forEach(f => {
                if (f.style && getComputedStyle(f).position !== 'absolute') {
                    f.style.transition = 'background 0.25s';
                }
            });
        });
    }
    const obs = new MutationObserver(apply);
    obs.observe(document.body, { subtree:true, childList:true, attributes:true, attributeFilter:['aria-valuenow','value'] });
    document.addEventListener('input', apply, true);
    [200,600,1200,2500].forEach(t => setTimeout(apply, t));
})();
</script>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Assess Button ─────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
if st.button("⬡  INITIATE RISK ASSESSMENT"):
    result     = engine.assess_risk(
        age=age, gender=gender,
        hb=hemoglobin, wbc=wbc,
        rbc=rbc, platelets=platelets,
        symptoms=symptoms
    )
    risk       = result['risk_level']
    risk_class = risk.lower()

    # ── Result ──
    st.markdown(f"""
    <div class="result-wrap {risk_class}">
        <div class="result-tag">// ASSESSMENT COMPLETE · RISK CLASSIFICATION</div>
        <div class="result-level {risk_class}">{risk.upper()}</div>
        <div class="urgency-chip">
            <span class="urgency-dot"></span>
            {result['urgency'].upper()}
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""
        <div class="card">
        <div class="card-header">
            <span class="card-header-num">—</span>
            <span class="card-header-title">Detected Abnormalities</span>
            <span class="card-header-line"></span>
        </div>
        """, unsafe_allow_html=True)
        if result["abnormalities"]:
            for i, ab in enumerate(result["abnormalities"], 1):
                st.markdown(
                    f'<div class="ab-item"><span class="ab-num">{i:02d}</span>{ab}</div>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                '<p style="font-family:var(--mono);font-size:0.75rem;color:#00ffaa;letter-spacing:0.1em;">'
                '[ NO ABNORMALITIES DETECTED ]</p>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="card">
        <div class="card-header">
            <span class="card-header-num">—</span>
            <span class="card-header-title">Clinical Recommendation</span>
            <span class="card-header-line"></span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="rec-box">{result["recommendation"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── CBC Chart ──
    st.markdown("""
    <div class="card">
    <div class="card-header">
        <span class="card-header-num">—</span>
        <span class="card-header-title">CBC vs Reference Range</span>
        <span class="card-header-line"></span>
        <span class="card-header-tag">COMPARATIVE ANALYSIS</span>
    </div>
    """, unsafe_allow_html=True)
    cbc_data = {
        "Parameter": ["Hemoglobin", "WBC", "Platelets"],
        "Patient Value": [hemoglobin, wbc, platelets],
        "Reference":     [
            NORMAL_CBC["Hemoglobin"][gender],
            NORMAL_CBC["WBC"],
            NORMAL_CBC["Platelets"]
        ]
    }
    df = pd.DataFrame(cbc_data).set_index("Parameter")
    st.bar_chart(df, color=["#ff2442", "#1a2535"])
    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    text-align:center;
    padding:2.5rem 0 1rem;
    font-family:'Share Tech Mono',monospace;
    font-size:0.62rem;
    letter-spacing:0.15em;
    color:#1e2a3a;
    border-top:1px solid rgba(255,36,66,0.08);
    margin-top:2rem;
">
    BLOODSCAN AI · FOR SCREENING PURPOSES ONLY · NOT A SUBSTITUTE FOR PROFESSIONAL MEDICAL ADVICE<br>
    <span style="color:#111d2a;">─────────────────────────────────────────────────</span>
</div>
""", unsafe_allow_html=True)