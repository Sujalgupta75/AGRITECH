# =====================================================
# TRAIN MODEL FILE
# =====================================================

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import pickle

print("\n🚀 Starting training process...")

# =====================================================
# STEP 1: LOAD DATA
# =====================================================

df = pd.read_csv(
    "C:\\Users\\sujal\\Downloads\\Harvestify-master\\Harvestify-master\\Data-raw\\raw_districtwise_yield_data.csv"
)

# =====================================================
# STEP 2: CLEAN BASIC PROBLEMS
# =====================================================

for col in ["State_Name", "District_Name", "Season", "Crop"]:
    df[col] = df[col].astype(str).str.strip().str.upper()

df = df.dropna(subset=["Area", "Production"])
df = df[df["Area"] > 0]

print("\n✅ Raw Seasons Found:", df["Season"].unique())

# =====================================================
# STEP 3: MAP SEASONS INTO 3 MAIN GROUPS
# =====================================================

def map_season(s):
    if s in ["KHARIF", "AUTUMN", "SUMMER"]:
        return "Kharif"
    if s in ["RABI", "WINTER"]:
        return "Rabi"
    if s == "WHOLE YEAR":
        return "Whole Year"
    return "Other"

df["Main_Season"] = df["Season"].apply(map_season)

print("\n✅ Mapped Seasons:", df["Main_Season"].unique())

# =====================================================
# STEP 4: COMPUTE YIELD
# =====================================================

df["Yield"] = df["Production"] / df["Area"]

# =====================================================
# STEP 5: AGGREGATE DATA
# =====================================================

agg = df.groupby(
    ["State_Name", "District_Name", "Crop", "Main_Season"]
).agg({
    "Yield": "mean",
    "Area": "mean",
    "Production": "mean",
    "Crop_Year": "count"
}).reset_index()

agg = agg.rename(columns={"Crop_Year": "Years_Grown"})

print("\n✅ Aggregated rows:", len(agg))

# =====================================================
# STEP 6: SUITABILITY SCORE
# =====================================================

agg["Suitability"] = (
    agg["Yield"] * 0.6 +
    agg["Area"] * 0.3 +
    agg["Years_Grown"] * 0.1
)

# =====================================================
# STEP 7: ENCODING
# =====================================================

le_state = LabelEncoder()
le_district = LabelEncoder()
le_crop = LabelEncoder()
le_season = LabelEncoder()

agg["state_enc"] = le_state.fit_transform(agg["State_Name"])
agg["district_enc"] = le_district.fit_transform(agg["District_Name"])
agg["crop_enc"] = le_crop.fit_transform(agg["Crop"])
agg["season_enc"] = le_season.fit_transform(agg["Main_Season"])

# =====================================================
# STEP 8: TRAIN MODEL
# =====================================================

X = agg[["state_enc", "district_enc", "crop_enc", "season_enc"]]
y = agg["Suitability"]

model = RandomForestRegressor()
model.fit(X, y)

print("\n✅ Model trained successfully!")

# =====================================================
# STEP 9: SAVE MODEL + LABEL ENCODERS + CLEAN DATA
# =====================================================

with open("crop_model.pkl", "wb") as f:
    pickle.dump({
        "model": model,
        "le_state": le_state,
        "le_district": le_district,
        "le_crop": le_crop,
        "le_season": le_season
    }, f)

agg.to_csv("clean_agg.csv", index=False)

print("\n✅ Model, encoders, and clean dataset saved successfully!")
print("➡ Saved files:")
print("   - crop_model.pkl")
print("   - clean_agg.csv")
