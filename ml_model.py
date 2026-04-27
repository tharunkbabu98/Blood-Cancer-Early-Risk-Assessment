import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib


def train_and_save_model(
    csv_path="/Users/tharunk/Desktop/cancer.detect/blood_cancer_risk_dataset copy.csv"
):
    # Load dataset
    df = pd.read_csv(csv_path)

    # =========================
    # Select Features
    # =========================
    feature_columns = [
        'hemoglobin', 'wbc_count', 'rbc_count', 'platelet_count',
        'fatigue', 'fever', 'weight_loss', 'night_sweats',
        'easy_bruising', 'frequent_infections',
        'lymph_node_swelling', 'bone_pain',
        'shortness_of_breath', 'bleeding_gums'
    ]

    X = df[feature_columns]
    y = df['risk_category']

    # Encode Target Labels

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    # Low - 0, Moderate - 1, High - 2

    
    # Train-Test Split
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    
    # Train Model

    model = RandomForestClassifier(
        n_estimators=150,
        random_state=42,
        class_weight='balanced'
    )
    model.fit(X_train, y_train)

  
    # Evaluation
   
    y_pred = model.predict(X_test)

    print("\nModel Accuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

   
    # Save Model
   
    joblib.dump(model, "risk_ml_model.pkl")
    joblib.dump(label_encoder, "label_encoder.pkl")

    print("\n Model and encoder saved successfully!")
    print("   Files created:")
    print("   - risk_ml_model.pkl")
    print("   - label_encoder.pkl")


if __name__ == "__main__":
    train_and_save_model()