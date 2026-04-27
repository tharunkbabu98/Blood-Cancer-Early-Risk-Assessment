class RiskAssessmentEngine:
  

    def __init__(self):
        self.normal_ranges = {
            'hemoglobin': { 'Male': (13.5, 17.5),
                'Female': (12.0, 15.5)
            },
            'wbc': (4.0, 11.0),
            'rbc': {
                'Male': (4.5, 5.9),
                'Female': (4.0, 5.2)
            },
            'platelets': (150, 400)
        }

    def assess_risk(self, age, gender, hb, wbc, rbc, platelets, symptoms):
        score = 0
        abnormalities = [] #list

        # Hemoglobin
        if hb < self.normal_ranges['hemoglobin'][gender][0]:
            score += 2
            abnormalities.append("Low Hemoglobin (Anemia)")

        # WBC
        if wbc < self.normal_ranges['wbc'][0] or wbc > self.normal_ranges['wbc'][1]:
            score += 2
            abnormalities.append("Abnormal WBC Count")

        # Platelets
        if platelets < self.normal_ranges['platelets'][0]:
            score += 3
            abnormalities.append("Low Platelet Count")

        # Symptoms
        symptom_score = sum(symptoms.values())
        score += symptom_score * 0.5

        # Final Risk Decision
        if score >= 10:
            risk = "High"
            urgency = "Urgent"
            recommendation = (
                " Immediate consultation with a hematologist is strongly recommended."
            )
        elif score >= 5:
            risk = "Moderate"
            urgency = "Soon"
            recommendation = (
                " Please consult a physician and consider repeating CBC tests."
            )
        else:
            risk = "Low"
            urgency = "Routine"
            recommendation = (
                " No immediate concern. Maintain routine health monitoring."
            )

        return {
            "risk_level": risk,
            "urgency": urgency,
            "abnormalities": abnormalities,
            "recommendation": recommendation
        }