from data_loader import load_dataset

df = load_dataset()

print("Dataset loaded successfully")
print("Shape:", df.shape)
print("\nColumns:")
print(df.columns)
print("\nFirst 5 rows:")
print(df.head())

print("\nRisk Category Distribution:")
print(df['risk_category'].value_counts())

print("\nCBC Summary (Hemoglobin):")
print(df.groupby('risk_category')['hemoglobin'].mean())

print("\nCBC Summary (WBC):")
print(df.groupby('risk_category')['wbc_count'].mean())

print("\nCBC Summary (Platelets):")
print(df.groupby('risk_category')['platelet_count'].mean())