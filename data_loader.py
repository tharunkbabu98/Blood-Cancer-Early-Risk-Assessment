import pandas as pd

def load_dataset(path="/Users/tharunk/Desktop/cancer.detect/blood_cancer_risk_dataset copy.csv"):
    df = pd.read_csv(path)
    return df