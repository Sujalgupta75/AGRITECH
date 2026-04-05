import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

# Load dataset
df = pd.read_csv(r"C:\Users\sujal\OneDrive\Desktop\ALL DATA\PYTHON\ML Projects\data_for_ml\CropDataset_with_avg_temp_rainfall_state_level.csv")

# ---------------- Features and Labels ----------------
X = df[["est_N", "est_P", "est_K", "estimated_pH", "Average_Rainfall_mm", "Average_Temperature"]]
y = df["Crop"]


# ---- Encoding the target (Crop) ----
# Option 1: LabelEncoder (recommended for single label)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# ---- Train-test split ----
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.05, random_state=42
)

# ---- Train classifier ----
model = RandomForestClassifier()
model.fit(X_train, y_train)

# ---- Example soil data ----
row = df.iloc[25]
sample = [[row["est_N"], row["est_P"], row["est_K"], row["estimated_pH"], row["Average_Rainfall_mm"],row["Average_Temperature"]]]

# ---- Predict ----
y_pred_encoded = model.predict(sample)
y_pred = label_encoder.inverse_transform(y_pred_encoded)

print("Recommended Crop:", y_pred[0])
