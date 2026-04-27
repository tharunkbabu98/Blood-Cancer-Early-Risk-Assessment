import streamlit as st
import pandas as pd
from risk_engine import RiskAssessmentEngine


# Page configuration
st.set_page_config(
    page_title="Blood Cancer Risk Assessment",
    page_icon="blood",
    layout="wide"
)



NORMAL_CBC = {
    "Hemoglobin": {
        "Male": 15.0,
        "Female": 13.5
    },
    "WBC": 7.5,        # ×10³
    "Platelets": 275  # ×10³
}

st.title(" Blood Cancer Early Risk Assessment System")

st.divider()


# Initialize Engine

engine = RiskAssessmentEngine()

with st.expander("Patient Details", expanded=True):
    age = st.number_input("Age", 18, 100, 30)
    gender = st.selectbox("Gender", ["Male", "Female"])

with st.expander(" Complete Blood Count (CBC)", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        hemoglobin = st.number_input("Hemoglobin (g/dL)", 4.0, 20.0, 13.5)
        wbc = st.number_input("WBC Count (×10³/μL)", 0.5, 100.0, 7.0)
    with col2:
        rbc = st.number_input("RBC Count (×10⁶/μL)", 1.5, 7.0, 4.5)
        platelets = st.number_input("Platelet Count (×10³/μL)", 10, 600, 250)

with st.expander("Clinical Symptoms (0 = None, 3 = Severe)", expanded=False):
    symptoms = {
        'fatigue': st.slider("Fatigue", 0, 3, 0),
        'fever': st.slider("Fever", 0, 3, 0),
        'weight_loss': st.slider("Weight Loss", 0, 3, 0),
        'night_sweats': st.slider("Night Sweats", 0, 3, 0),
        'easy_bruising': st.slider("Easy Bruising", 0, 3, 0),
        'frequent_infections': st.slider("Frequent Infections", 0, 3, 0),
        'lymph_node_swelling': st.slider("Lymph Node Swelling", 0, 3, 0),
        'bone_pain': st.slider("Bone Pain", 0, 3, 0),
        'shortness_of_breath': st.slider("Shortness of Breath", 0, 3, 0),
        'bleeding_gums': st.slider("Bleeding Gums", 0, 3, 0),
    }

st.divider()


# Run Assessment

if st.button(" Assess Risk"):
    result = engine.assess_risk(
        age=age,
        gender=gender,
        hb=hemoglobin,
        wbc=wbc,
        rbc=rbc,
        platelets=platelets,
        symptoms=symptoms
    )

    st.subheader(" Risk Assessment Result")

    # Risk level display
    color_map = {"Low": "green", "Moderate": "orange", "High": "red"}
    st.markdown(
        f"### Risk Level: "
        f"<span style='color:{color_map[result['risk_level']]};'>"
        f"{result['risk_level']}</span>",
        unsafe_allow_html=True
    )

    st.write("**Urgency:**", result["urgency"])

    # Abnormalities
    if result["abnormalities"]:
        st.warning("### Detected Abnormalities")
        for ab in result["abnormalities"]:
            st.write(f"• {ab}")

    # Recommendation
    st.success("### Recommendation")
    st.write(result["recommendation"])

    st.divider()
    st.subheader(" CBC Comparison with Normal Range")

    cbc_data = {
        "Parameter": ["Hemoglobin", "WBC", "Platelets"],
        "Your Value": [
            hemoglobin,
            wbc,
            platelets
        ],
        "Normal Value": [
            NORMAL_CBC["Hemoglobin"][gender],
            NORMAL_CBC["WBC"],
            NORMAL_CBC["Platelets"]
        ]
    }

    df_cbc_chart = pd.DataFrame(cbc_data)
    df_cbc_chart.set_index("Parameter", inplace=True)

    st.bar_chart(df_cbc_chart)
