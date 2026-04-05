# =====================================================
# PREDICTION FILE
# =====================================================

import pandas as pd
import pickle

# =====================================================
# LOAD MODEL + ENCODERS + CLEAN DATA
# =====================================================

with open("crop_model.pkl", "rb") as f:
    data = pickle.load(f)

model = data["model"]
le_state = data["le_state"]
le_district = data["le_district"]
le_crop = data["le_crop"]
le_season = data["le_season"]

agg = pd.read_csv("clean_agg.csv")

# =====================================================
# RECOMMENDATION FUNCTION
# =====================================================

def recommend_crops(state, district):

    state = state.upper().strip()
    district = district.upper().strip()

    if district not in agg["District_Name"].unique():
        print("\n ❌ District NOT FOUND in dataset:", district)
        return {"Kharif": [], "Rabi": [], "Whole Year": []}

    results = {}
    seasons_to_use = ["Kharif", "Rabi", "Whole Year"]

    for season in seasons_to_use:

        temp = agg[
            (agg["State_Name"] == state) &
            (agg["District_Name"] == district) &
            (agg["Main_Season"] == season)
        ]

        if temp.empty:
            results[season] = []
            continue

        X_pred = pd.DataFrame({
            "state_enc": le_state.transform(temp["State_Name"]),
            "district_enc": le_district.transform(temp["District_Name"]),
            "crop_enc": le_crop.transform(temp["Crop"]),
            "season_enc": le_season.transform(temp["Main_Season"])
        })

        temp["PredictedScore"] = model.predict(X_pred)

        top_crops = temp.sort_values(
            "PredictedScore", ascending=False
        ).head(5)["Crop"].tolist()

        results[season] = top_crops

    return results

# =====================================================
# USER INPUT SECTION
# =====================================================

if __name__ == "__main__":
    state = input("Enter your state name: ").strip()
    district = input("Enter your district name: ").strip()

    output = recommend_crops(state, district)

    print("\n✅ RECOMMENDED CROPS FOR:", district)
    print("\nKharif:", output["Kharif"])
    print("Rabi:", output["Rabi"])
    print("Whole Year:", output["Whole Year"])
