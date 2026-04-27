import streamlit as st
import pandas as pd
from risk_engine import RiskAssessmentEngine

# Page configuration
st.set_page_config(
    page_title="BloodScan AI · Risk Assessment",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #080c14 !important;
    color: #e8edf5 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(220,38,38,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(220,38,38,0.08) 0%, transparent 60%),
        #080c14 !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none; }
section[data-testid="stMain"] > div { padding-top: 0 !important; }
.block-container { padding: 0 2rem 4rem !important; max-width: 1100px !important; margin: 0 auto; }

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 3.5rem 2rem 2rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    background: rgba(220,38,38,0.15);
    border: 1px solid rgba(220,38,38,0.35);
    color: #f87171;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 999px;
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: clamp(2rem, 5vw, 3.2rem) !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    line-height: 1.1 !important;
    letter-spacing: -0.02em !important;
    margin-bottom: 0.8rem !important;
}
.hero h1 span { color: #ef4444; }
.hero p {
    font-size: 1rem;
    color: #8892a4;
    max-width: 520px;
    margin: 0 auto 2rem;
    line-height: 1.6;
}
.hero-divider {
    width: 60px; height: 3px;
    background: linear-gradient(90deg, #ef4444, #f97316);
    border-radius: 2px;
    margin: 0 auto 2.5rem;
}

/* ── Section Cards ── */
.section-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(10px);
    transition: border-color 0.2s;
}
.section-card:hover { border-color: rgba(239,68,68,0.25); }

.section-label {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #ef4444;
    margin-bottom: 1.3rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(239,68,68,0.2);
}

/* ── Inputs ── */
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e8edf5 !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stNumberInput"] input:focus,
[data-testid="stSelectbox"] > div > div:focus {
    border-color: rgba(239,68,68,0.5) !important;
    box-shadow: 0 0 0 3px rgba(239,68,68,0.1) !important;
}

label, [data-testid="stWidgetLabel"] {
    color: #a0aab8 !important;
    font-size: 0.85rem !important;
    font-weight: 400 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Sliders base ── */
[data-testid="stSlider"] > div > div > div {
    background: rgba(239,68,68,0.2) !important;
}
[data-testid="stSlider"] > div > div > div > div {
    background: #ef4444 !important;
    box-shadow: 0 0 10px rgba(239,68,68,0.4) !important;
    transition: background 0.3s, box-shadow 0.3s !important;
}

/* ── Assess Button ── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #ef4444, #dc2626) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.9rem 2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 20px rgba(239,68,68,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(239,68,68,0.45) !important;
}

/* ── Result Cards ── */
.result-hero {
    border-radius: 16px;
    padding: 2rem;
    margin: 1.5rem 0;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.result-hero.low {
    background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(16,185,129,0.05));
    border: 1px solid rgba(16,185,129,0.3);
}
.result-hero.moderate {
    background: linear-gradient(135deg, rgba(245,158,11,0.15), rgba(245,158,11,0.05));
    border: 1px solid rgba(245,158,11,0.3);
}
.result-hero.high {
    background: linear-gradient(135deg, rgba(239,68,68,0.2), rgba(239,68,68,0.05));
    border: 1px solid rgba(239,68,68,0.4);
}
.risk-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    opacity: 0.7;
    margin-bottom: 0.4rem;
}
.risk-value {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 0.5rem;
}
.risk-value.low  { color: #10b981; }
.risk-value.moderate { color: #f59e0b; }
.risk-value.high { color: #ef4444; }

.info-pill {
    display: inline-block;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 999px;
    padding: 0.3rem 0.9rem;
    font-size: 0.8rem;
    color: #a0aab8;
    margin-top: 0.6rem;
}

.abnormality-item {
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.2);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
    color: #fca5a5;
}
.abnormality-dot {
    width: 6px; height: 6px;
    background: #ef4444;
    border-radius: 50%;
    margin-top: 6px;
    flex-shrink: 0;
}

.recommendation-box {
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    color: #6ee7b7;
    font-size: 0.92rem;
    line-height: 1.6;
}

hr { border-color: rgba(255,255,255,0.07) !important; }
[data-testid="stExpander"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge"> AI-Powered Hematology Screening</div>
    <h1>Blood<span>Scan</span> AI</h1>
    <p>Early risk assessment for blood cancers using CBC values, patient demographics, and clinical symptom analysis.</p>
    <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)

NORMAL_CBC = {
    "Hemoglobin": {"Male": 15.0, "Female": 13.5},
    "WBC": 7.5,
    "Platelets": 275
}

engine = RiskAssessmentEngine()

# ── Patient Details ───────────────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">👤 Patient Details</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", 18, 100, 30)
with col2:
    gender = st.selectbox("Gender", ["Male", "Female"])
st.markdown('</div>', unsafe_allow_html=True)

# ── CBC ───────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">🔬 Complete Blood Count (CBC)</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    hemoglobin = st.number_input("Hemoglobin (g/dL)", 4.0, 20.0, 13.5)
    wbc = st.number_input("WBC Count (×10³/μL)", 0.5, 100.0, 7.0)
with col2:
    rbc = st.number_input("RBC Count (×10⁶/μL)", 1.5, 7.0, 4.5)
    platelets = st.number_input("Platelet Count (×10³/μL)", 10, 600, 250)
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
severity_colors = {0: "#4b5563", 1: "#f97316", 2: "#ef4444", 3: "#dc2626"}

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown("""
<div class="section-label">
    🩺 Clinical Symptoms
    <span style="font-weight:300;color:#8892a4;font-size:0.7rem;letter-spacing:0;text-transform:none;">
        &nbsp;0 = None &nbsp;·&nbsp; 3 = Severe
    </span>
</div>
""", unsafe_allow_html=True)

symptoms = {}
half = len(symptom_list) // 2
col1, col2 = st.columns(2)

with col1:
    for key, label in symptom_list[:half]:
        val = st.slider(label, 0, 3, 0, key=key)
        symptoms[key] = val
        color = severity_colors[val]
        sev = severity_labels[val]
        st.markdown(
            f'<div style="margin:-14px 0 12px;text-align:right;">'
            f'<span style="font-size:0.72rem;font-weight:600;color:{color};">{sev}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

with col2:
    for key, label in symptom_list[half:]:
        val = st.slider(label, 0, 3, 0, key=key)
        symptoms[key] = val
        color = severity_colors[val]
        sev = severity_labels[val]
        st.markdown(
            f'<div style="margin:-14px 0 12px;text-align:right;">'
            f'<span style="font-size:0.72rem;font-weight:600;color:{color};">{sev}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

# ── Dynamic slider color JS ───────────────────────────────────────────────────
st.markdown("""
<script>
(function() {
    const trackColors = {
        0: 'rgba(75,85,99,0.4)',
        1: 'rgba(249,115,22,0.5)',
        2: 'rgba(239,68,68,0.7)',
        3: 'rgba(220,38,38,1.0)'
    };
    const thumbGlow = {
        0: 'none',
        1: '0 0 8px rgba(249,115,22,0.5)',
        2: '0 0 12px rgba(239,68,68,0.6)',
        3: '0 0 18px rgba(220,38,38,0.9)'
    };
    const thumbColor = {
        0: '#4b5563',
        1: '#f97316',
        2: '#ef4444',
        3: '#dc2626'
    };

    function applyColors() {
        document.querySelectorAll('[data-testid="stSlider"]').forEach(sliderWidget => {
            const input = sliderWidget.querySelector('input[type="range"]');
            if (!input) return;
            const val = Math.round(parseFloat(input.value)) || 0;
            const clampedVal = Math.min(3, Math.max(0, val));

            // Style the track fill
            const trackFill = sliderWidget.querySelector('div[data-baseweb="slider"] > div > div:first-child');
            if (trackFill) {
                trackFill.style.background = trackColors[clampedVal];
            }

            // Style the thumb
            const thumb = sliderWidget.querySelector('[role="slider"]');
            if (thumb) {
                thumb.style.background = thumbColor[clampedVal];
                thumb.style.boxShadow  = thumbGlow[clampedVal];
                thumb.style.transition = 'background 0.3s, box-shadow 0.3s';
            }

            // Native accent color fallback
            input.style.accentColor = thumbColor[clampedVal];
        });
    }

    const observer = new MutationObserver(applyColors);
    observer.observe(document.body, {
        subtree: true,
        childList: true,
        attributes: true,
        attributeFilter: ['aria-valuenow', 'value']
    });
    document.addEventListener('input', applyColors, true);
    [300, 800, 1500, 3000].forEach(t => setTimeout(applyColors, t));
})();
</script>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Assess Button ─────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔍 Run Risk Assessment"):
    result = engine.assess_risk(
        age=age, gender=gender,
        hb=hemoglobin, wbc=wbc,
        rbc=rbc, platelets=platelets,
        symptoms=symptoms
    )

    risk = result['risk_level']
    risk_class = risk.lower()

    # ── Result Hero ──
    st.markdown(f"""
    <div class="result-hero {risk_class}">
        <div class="risk-label">Assessment Result</div>
        <div class="risk-value {risk_class}">{risk} Risk</div>
        <div class="info-pill">⚡ {result['urgency']}</div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        if result["abnormalities"]:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-label"> Detected Abnormalities</div>', unsafe_allow_html=True)
            for ab in result["abnormalities"]:
                st.markdown(
                    f'<div class="abnormality-item">'
                    f'<div class="abnormality-dot"></div>{ab}'
                    f'</div>',
                    unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="section-card">
                <div class="section-label"> Abnormalities</div>
                <p style="color:#6ee7b7;font-size:0.9rem;">No significant abnormalities detected in CBC values.</p>
            </div>
            """, unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label"> Recommendation</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="recommendation-box">{result["recommendation"]}</div>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # ── CBC Chart ──
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label"> CBC vs Normal Range</div>', unsafe_allow_html=True)
    cbc_data = {
        "Parameter": ["Hemoglobin", "WBC", "Platelets"],
        "Your Value": [hemoglobin, wbc, platelets],
        "Normal Value": [
            NORMAL_CBC["Hemoglobin"][gender],
            NORMAL_CBC["WBC"],
            NORMAL_CBC["Platelets"]
        ]
    }
    df = pd.DataFrame(cbc_data).set_index("Parameter")
    st.bar_chart(df, color=["#ef4444", "#374151"])
    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem 0 1rem;color:#3d4a5c;font-size:0.78rem;">
    BloodScan AI · For screening purposes only · Not a substitute for professional medical advice
</div>
""", unsafe_allow_html=True)