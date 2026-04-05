# =====================================================
# Django Views – Crop Recommendation Integrated
# =====================================================

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd
import pickle
import os
from django.http import JsonResponse
import json


# =====================================================
# LOAD MODEL & DATA ONCE WHEN SERVER STARTS
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, "crop_model.pkl"), "rb") as f:
    data = pickle.load(f)

model = data["model"]
le_state = data["le_state"]
le_district = data["le_district"]
le_crop = data["le_crop"]
le_season = data["le_season"]

agg = pd.read_csv(os.path.join(BASE_DIR, "clean_agg.csv"))

# Normalize columns
agg["State_Name"] = agg["State_Name"].str.upper()
agg["District_Name"] = agg["District_Name"].str.upper()
agg["Main_Season"] = agg["Main_Season"].str.title()


# =====================================================
# CROP RECOMMENDATION FUNCTION
# =====================================================

def recommend_crops(state, district):

    state = state.upper().strip()
    district = district.upper().strip()

    # District Validation
    if district not in agg["District_Name"].unique():
        return {
            "error": f"District '{district}' not found in the database.",
            "Kharif": [],
            "Rabi": [],
            "Whole Year": [],
        }

    results = {}
    seasons = ["Kharif", "Rabi", "Whole Year"]

    for season in seasons:

        filtered = agg[
            (agg["State_Name"] == state)
            & (agg["District_Name"] == district)
            & (agg["Main_Season"] == season)
        ]

        if filtered.empty:
            results[season] = []
            continue

        # Prepare input for model
        X = pd.DataFrame({
            "state_enc": le_state.transform(filtered["State_Name"]),
            "district_enc": le_district.transform(filtered["District_Name"]),
            "crop_enc": le_crop.transform(filtered["Crop"]),
            "season_enc": le_season.transform(filtered["Main_Season"])
        })

        filtered["PredictedScore"] = model.predict(X)

        # Top 5 crops
        results[season] = (
            filtered.sort_values("PredictedScore", ascending=False)
            .head(5)["Crop"]
            .tolist()
        )

    return results


# =====================================================
# LIST CROP PAGE
# =====================================================

@login_required(login_url='/login/')
def listcrop(request):

    context = {}

    # Get states for dropdown
    states = sorted(agg["State_Name"].unique())
    context["states"] = states

    # Create dict → { "UTTAR PRADESH": ["KANPUR", "LUCKNOW", ...] }
    district_map = (
        agg.groupby("State_Name")["District_Name"]
           .unique()
           .apply(list)
           .to_dict()
    )

    # Pass district JSON to template for JavaScript
    context["district_json"] = json.dumps(district_map)

    # Default empty district list for template
    context["districts"] = []

    if request.method == "POST":
        state = request.POST.get("state")
        district = request.POST.get("district")

        context["selected_state"] = state
        context["selected_district"] = district

        # Fill districts in dropdown when POST reloads page
        if state:
            context["districts"] = district_map.get(state.upper(), [])

        output = recommend_crops(state, district)

        if "error" in output:
            context["error"] = output["error"]
        else:
            context["kharif"] = output["Kharif"]
            context["rabi"] = output["Rabi"]
            context["whole"] = output["Whole Year"]

    return render(request, "html/listcrop.html", context)


# =====================================================
# AJAX API FOR DISTRICT FILTERING (OPTIONAL)
# =====================================================

def get_districts(request):
    state = request.GET.get("state", "").upper()

    district_map = (
        agg.groupby("State_Name")["District_Name"]
           .unique()
           .apply(list)
           .to_dict()
    )

    districts = district_map.get(state, [])
    return JsonResponse({"districts": districts})


# =====================================================
# OTHER ROUTES
# =====================================================

@login_required(login_url='/login/')
def home(request):
    return render(request, 'html/home1.html')


