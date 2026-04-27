from risk_engine import RiskAssessmentEngine

engine = RiskAssessmentEngine()

result = engine.assess_risk(
    age=45,
    gender="Male",
    hb=9.0,
    wbc=15.0,
    rbc=3.5,
    platelets=120,
    symptoms={
        'fatigue': 2,
        'fever': 1,
        'weight_loss': 1,
        'night_sweats': 0,
        'easy_bruising': 1,
        'frequent_infections': 1,
        'lymph_node_swelling': 0,
        'bone_pain': 0,
        'shortness_of_breath': 1,
        'bleeding_gums': 0
    }
)

print(result)