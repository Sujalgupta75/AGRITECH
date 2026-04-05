import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# ---------------- Load dataset ----------------
df = pd.read_csv(r"C:\\Users\sujal\OneDrive\Desktop\ALL DATA\PYTHON\ML Projects\data_for_ml\CropDataset_with_avg_temp_rainfall_state_level.csv")

# ---------------- Features and Labels ----------------
X = df[["est_N", "est_P", "est_K", "estimated_pH", "Average_Rainfall_mm", "Average_Temperature"]]
y = df["Crop"]

# ---------------- Encode the target labels ----------------
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# ---------------- Split dataset ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# ---------------- Train the Random Forest Classifier ----------------
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# ---------------- Check Model Accuracy ----------------
y_pred_test = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred_test)
print(f"✅ Model Accuracy: {accuracy*100:.2f}%\n")

# ---------------- Example: Input Sample ----------------
df1= pd.read_csv("C:\\Users\sujal\OneDrive\Desktop\ALL DATA\PYTHON\ML Projects\data_for_ml\CropDataset_Final_with_estimated_pH.csv")
row = df1.iloc[100]  # 26th row
sample = [[row["est_N"], row["est_P"], row["est_K"], row["estimated_pH"], 2363, 24]]

# ---------------- Get Probabilities for All Crops ----------------
probs = model.predict_proba(sample)[0]  # Probability for each crop
sorted_idx = np.argsort(probs)[::-1]   # Sort from highest to lowest
sorted_crops = label_encoder.inverse_transform(sorted_idx)
sorted_probs = probs[sorted_idx]

# ---------------- Display All Crops Sorted by Confidence ----------------
print("🌾 All Possible Crop Recommendations (Ranked):")
for rank, (crop, prob) in enumerate(zip(sorted_crops, sorted_probs), start=1):
    print(f"{rank}. {crop:<20}  — Confidence: {prob*100:.2f}%")
