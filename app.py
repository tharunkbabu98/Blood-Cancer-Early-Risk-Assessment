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
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Outfit:wght@300;400;500;600&display=swap');

:root {
    --red:      #e8354a;
    --red-soft: rgba(232,53,74,0.12);
    --red-glow: rgba(232,53,74,0.25);
    --gold:     #c9a96e;
    --green:    #2dd4a0;
    --amber:    #e8a435;
    --bg:       #080b10;
    --bg2:      #0d1018;
    --card:     rgba(255,255,255,0.028);
    --border:   rgba(255,255,255,0.07);
    --border-r: rgba(232,53,74,0.22);
    --text:     #d4dce8;
    --muted:    #5c6a7e;
    --serif:    'Cormorant Garamond', Georgia, serif;
    --sans:     'Outfit', sans-serif;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
}

/* Rich multi-layer background */
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 100% 55% at 0% 0%,   rgba(232,53,74,0.09)  0%, transparent 60%),
        radial-gradient(ellipse 70%  50% at 100% 80%, rgba(201,169,110,0.05) 0%, transparent 55%),
        radial-gradient(ellipse 60%  40% at 50%  50%, rgba(10,20,40,0.8)    0%, transparent 70%),
        var(--bg) !important;
}

[data-testid="stHeader"]  { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }
section[data-testid="stMain"] > div { padding-top: 0 !important; }
.block-container {
    padding: 0 3rem 5rem !important;
    max-width: 1080px !important;
    margin: 0 auto;
}

/* ── Hero ── */
.hero {
    padding: 4.5rem 1rem 3rem;
    text-align: center;
}

.hero-pre {
    display: inline-flex;
    align-items: center;
    gap: 0.7rem;
    font-family: var(--sans);
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 1.4rem;
    opacity: 0.85;
}
.hero-pre::before,
.hero-pre::after {
    content: '';
    display: inline-block;
    width: 28px;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold));
}
.hero-pre::after { transform: scaleX(-1); }

.hero-title {
    font-family: var(--serif) !important;
    font-size: clamp(3rem, 7vw, 5.5rem) !important;
    font-weight: 300 !important;
    color: #ffffff !important;
    letter-spacing: 0.04em !important;
    line-height: 0.95 !important;
    margin-bottom: 1rem !important;
}
.hero-title strong {
    font-weight: 600;
    color: var(--red);
    font-style: italic;
}

.hero-sub {
    font-family: var(--sans);
    font-size: 0.8rem;
    font-weight: 400;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 1.5rem;
}

.hero-desc {
    font-family: var(--sans);
    font-size: 0.95rem;
    font-weight: 300;
    color: #7a8a9e;
    max-width: 460px;
    margin: 0 auto 2.5rem;
    line-height: 1.8;
}

.hero-ornament {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    margin: 0 auto 0;
    opacity: 0.4;
}
.hero-ornament span { width: 60px; height: 1px; background: linear-gradient(90deg, transparent, var(--red)); }
.hero-ornament span:last-child { transform: scaleX(-1); }
.hero-ornament i { width: 5px; height: 5px; border-radius: 50%; background: var(--red); }

/* ── Cards ── */
.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.1rem;
    backdrop-filter: blur(20px);
    transition: border-color 0.35s, box-shadow 0.35s;
    position: relative;
    overflow: hidden;
}
.card::before {
    content: '';
    position: absolute;
    top: 0; left: 10%; right: 10%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(232,53,74,0.4), transparent);
}
.card:hover {
    border-color: var(--border-r);
    box-shadow: 0 8px 40px rgba(0,0,0,0.3), 0 0 0 1px rgba(232,53,74,0.06);
}

.card-heading {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.6rem;
}
.card-heading-icon {
    width: 32px; height: 32px;
    border-radius: 8px;
    background: var(--red-soft);
    border: 1px solid var(--border-r);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.95rem;
    flex-shrink: 0;
}
.card-heading-text {
    font-family: var(--sans);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--text);
    opacity: 0.7;
}
.card-heading-line {
    flex: 1; height: 1px;
    background: linear-gradient(90deg, var(--border-r), transparent);
}

/* ── Inputs ── */
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.035) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 8px !important;
    color: #e0e8f4 !important;
    font-family: var(--sans) !important;
    font-size: 0.95rem !important;
    font-weight: 400 !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: rgba(232,53,74,0.5) !important;
    box-shadow: 0 0 0 3px rgba(232,53,74,0.1) !important;
    background: rgba(232,53,74,0.04) !important;
}

label, [data-testid="stWidgetLabel"] p {
    font-family: var(--sans) !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    color: #5c6a7e !important;
    text-transform: none !important;
}

/* ── Sliders ── */
[data-testid="stSlider"] > div > div > div {
    background: rgba(255,255,255,0.07) !important;
    height: 3px !important;
    border-radius: 2px !important;
}
[data-testid="stSlider"] > div > div > div > div {
    background: var(--red) !important;
    box-shadow: 0 0 12px rgba(232,53,74,0.5) !important;
    transition: background 0.3s, box-shadow 0.3s !important;
}

/* ── Button ── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--red), #c0293c) !important;
    border: none !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-family: var(--sans) !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    padding: 1rem 2rem !important;
    cursor: pointer !important;
    transition: all 0.3s !important;
    box-shadow: 0 4px 24px rgba(232,53,74,0.3), 0 1px 0 rgba(255,255,255,0.1) inset !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 40px rgba(232,53,74,0.45), 0 1px 0 rgba(255,255,255,0.15) inset !important;
    letter-spacing: 0.18em !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Result ── */
.result-card {
    border-radius: 12px;
    padding: 3rem 2rem;
    margin: 1.8rem 0;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.result-card.low {
    background: radial-gradient(ellipse at center, rgba(45,212,160,0.1) 0%, rgba(45,212,160,0.02) 70%);
    border: 1px solid rgba(45,212,160,0.25);
}
.result-card.moderate {
    background: radial-gradient(ellipse at center, rgba(232,164,53,0.1) 0%, rgba(232,164,53,0.02) 70%);
    border: 1px solid rgba(232,164,53,0.3);
}
.result-card.high {
    background: radial-gradient(ellipse at center, rgba(232,53,74,0.14) 0%, rgba(232,53,74,0.02) 70%);
    border: 1px solid rgba(232,53,74,0.35);
}

.result-eyebrow {
    font-family: var(--sans);
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.8rem;
}

.result-title {
    font-family: var(--serif);
    font-size: clamp(2.8rem, 7vw, 5rem);
    font-weight: 300;
    font-style: italic;
    line-height: 1;
    margin-bottom: 1rem;
    letter-spacing: 0.02em;
}
.result-title.low      { color: var(--green); text-shadow: 0 0 40px rgba(45,212,160,0.4); }
.result-title.moderate { color: var(--amber); text-shadow: 0 0 40px rgba(232,164,53,0.4); }
.result-title.high     { color: var(--red);   text-shadow: 0 0 40px rgba(232,53,74,0.5); }

.result-urgency {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 999px;
    padding: 0.45rem 1.2rem;
    font-family: var(--sans);
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    color: var(--muted);
}
.urgency-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--red);
    box-shadow: 0 0 8px var(--red);
    animation: pulse 2s ease-in-out infinite;
}
.result-card.low    .urgency-dot { background: var(--green); box-shadow: 0 0 8px var(--green); }
.result-card.moderate .urgency-dot { background: var(--amber); box-shadow: 0 0 8px var(--amber); }
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.4;transform:scale(0.85)} }

/* ── Abnormalities ── */
.ab-wrap { display: flex; flex-direction: column; gap: 0.45rem; }
.ab-item {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    background: rgba(232,53,74,0.05);
    border: 1px solid rgba(232,53,74,0.12);
    border-radius: 8px;
    padding: 0.8rem 1rem;
    font-family: var(--sans);
    font-size: 0.88rem;
    font-weight: 400;
    color: #e0a0a8;
    line-height: 1.5;
    transition: background 0.2s;
}
.ab-item:hover { background: rgba(232,53,74,0.09); }
.ab-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--red);
    margin-top: 6px;
    flex-shrink: 0;
    box-shadow: 0 0 6px rgba(232,53,74,0.6);
}

/* ── Recommendation ── */
.rec-box {
    background: rgba(45,212,160,0.05);
    border: 1px solid rgba(45,212,160,0.18);
    border-left: 3px solid var(--green);
    border-radius: 8px;
    padding: 1.3rem 1.5rem;
    font-family: var(--sans);
    font-size: 0.92rem;
    font-weight: 400;
    color: #90e8cc;
    line-height: 1.8;
}

/* ── Severity badge ── */
.sev-badge {
    font-family: var(--sans);
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    text-align: right;
    margin: -10px 0 12px;
    transition: color 0.3s;
}

/* ── No abnormalities ── */
.no-ab {
    font-family: var(--sans);
    font-size: 0.88rem;
    color: var(--green);
    opacity: 0.8;
    padding: 0.5rem 0;
}

hr { border-color: rgba(255,255,255,0.05) !important; }
[data-testid="stExpander"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-pre">Hematological Risk Assessment</div>
    <h1 class="hero-title">Blood<strong>Scan</strong> AI</h1>
    <div class="hero-sub">Early Detection · Machine Learning · Clinical Insight</div>
    <p class="hero-desc">
        Advanced analysis of complete blood count values paired with clinical
        symptom patterns to identify early indicators of hematological risk.
    </p>
    <div class="hero-ornament">
        <span></span><i></i><i style="opacity:0.5;width:3px;height:3px"></i><i></i><span></span>
    </div>
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
<div class="card-heading">
    <div class="card-heading-icon">👤</div>
    <div class="card-heading-text">Patient Profile</div>
    <div class="card-heading-line"></div>
</div>
""", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age (years)", 18, 100, 30)
with col2:
    gender = st.selectbox("Biological Sex", ["Male", "Female"])
st.markdown('</div>', unsafe_allow_html=True)

# ── CBC ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="card">
<div class="card-heading">
    <div class="card-heading-icon">🔬</div>
    <div class="card-heading-text">Complete Blood Count</div>
    <div class="card-heading-line"></div>
</div>
""", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    hemoglobin = st.number_input("Hemoglobin (g/dL)", 4.0, 20.0, 13.5)
    wbc        = st.number_input("WBC Count (×10³/μL)", 0.5, 100.0, 7.0)
with col2:
    rbc        = st.number_input("RBC Count (×10⁶/μL)", 1.5, 7.0, 4.5)
    platelets  = st.number_input("Platelet Count (×10³/μL)", 10, 600, 250)
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

severity_labels = {0: "None", 1: "Mild", 2: "Moderate", 3: "Severe"}
severity_colors = {0: "#2e3a4a", 1: "#d97706", 2: "#e8354a", 3: "#c0293c"}
severity_glow   = {
    0: "none",
    1: "0 0 8px rgba(217,119,6,0.5)",
    2: "0 0 12px rgba(232,53,74,0.55)",
    3: "0 0 18px rgba(192,41,60,0.8)"
}

st.markdown("""
<div class="card">
<div class="card-heading">
    <div class="card-heading-icon">🩺</div>
    <div class="card-heading-text">Clinical Symptoms</div>
    <div class="card-heading-line"></div>
</div>
<p style="font-family:'Outfit',sans-serif;font-size:0.78rem;color:#3e4e62;margin:-0.5rem 0 1.5rem;font-weight:400;letter-spacing:0.04em;">
    Rate each symptom from 0 (not present) to 3 (severe)
</p>
""", unsafe_allow_html=True)

symptoms = {}
half = len(symptom_list) // 2
col1, col2 = st.columns(2)

with col1:
    for key, label in symptom_list[:half]:
        val = st.slider(label, 0, 3, 0, key=key)
        symptoms[key] = val
        c = severity_colors[val]
        s = severity_labels[val]
        st.markdown(
            f'<div class="sev-badge" style="color:{c};text-shadow:{severity_glow[val]};">{s}</div>',
            unsafe_allow_html=True
        )

with col2:
    for key, label in symptom_list[half:]:
        val = st.slider(label, 0, 3, 0, key=key)
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
    const thumbColor = { 0:'#2e3a4a', 1:'#d97706', 2:'#e8354a', 3:'#c0293c' };
    const thumbGlow  = {
        0:'none',
        1:'0 0 10px rgba(217,119,6,0.55)',
        2:'0 0 14px rgba(232,53,74,0.65)',
        3:'0 0 22px rgba(192,41,60,0.9), 0 0 40px rgba(192,41,60,0.3)'
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
                thumb.style.transition  = 'background 0.3s, box-shadow 0.3s';
            }
        });
    }
    const obs = new MutationObserver(apply);
    obs.observe(document.body, { subtree:true, childList:true, attributes:true, attributeFilter:['aria-valuenow','value'] });
    document.addEventListener('input', apply, true);
    [300, 800, 1500, 3000].forEach(t => setTimeout(apply, t));
})();
</script>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Assess Button ─────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
if st.button("Run Risk Assessment"):
    result     = engine.assess_risk(
        age=age, gender=gender,
        hb=hemoglobin, wbc=wbc,
        rbc=rbc, platelets=platelets,
        symptoms=symptoms
    )
    risk       = result['risk_level']
    risk_class = risk.lower()

    st.markdown(f"""
    <div class="result-card {risk_class}">
        <div class="result-eyebrow">Risk Classification</div>
        <div class="result-title {risk_class}">{risk} Risk</div>
        <div class="result-urgency">
            <span class="urgency-dot"></span>
            {result['urgency']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""
        <div class="card">
        <div class="card-heading">
            <div class="card-heading-icon">⚠️</div>
            <div class="card-heading-text">Detected Abnormalities</div>
            <div class="card-heading-line"></div>
        </div>
        <div class="ab-wrap">
        """, unsafe_allow_html=True)
        if result["abnormalities"]:
            for ab in result["abnormalities"]:
                st.markdown(
                    f'<div class="ab-item"><span class="ab-dot"></span>{ab}</div>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown('<p class="no-ab">✓ No significant abnormalities detected</p>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="card">
        <div class="card-heading">
            <div class="card-heading-icon">💊</div>
            <div class="card-heading-text">Clinical Recommendation</div>
            <div class="card-heading-line"></div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="rec-box">{result["recommendation"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <div class="card-heading">
        <div class="card-heading-icon">📊</div>
        <div class="card-heading-text">CBC vs Reference Range</div>
        <div class="card-heading-line"></div>
    </div>
    """, unsafe_allow_html=True)
    cbc_data = {
        "Parameter": ["Hemoglobin", "WBC", "Platelets"],
        "Your Value": [hemoglobin, wbc, platelets],
        "Reference":  [
            NORMAL_CBC["Hemoglobin"][gender],
            NORMAL_CBC["WBC"],
            NORMAL_CBC["Platelets"]
        ]
    }
    df = pd.DataFrame(cbc_data).set_index("Parameter")
    st.bar_chart(df, color=["#e8354a", "#1e2a38"])
    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    text-align:center;
    padding:3rem 0 1.5rem;
    font-family:'Outfit',sans-serif;
    font-size:0.72rem;
    font-weight:400;
    letter-spacing:0.1em;
    color:#1e2a38;
    border-top:1px solid rgba(255,255,255,0.04);
    margin-top:2rem;
">
    BloodScan AI &nbsp;·&nbsp; For screening purposes only &nbsp;·&nbsp; Not a substitute for professional medical advice
</div>
""", unsafe_allow_html=True)