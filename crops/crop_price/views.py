from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd
from catboost import CatBoostRegressor
from django.http import JsonResponse

# Load model
model = CatBoostRegressor()
model.load_model("crop_price_model.cbm")

# Load dataset
df = pd.read_csv("Agriculture_price_dataset.csv")


@login_required(login_url='/login/')
def home(request):
    return render(request, 'html/home.html')


def get_districts(request):
    state = request.GET.get("state")
    districts = df[df["STATE"] == state]["District Name"].dropna().unique().tolist()
    return JsonResponse({"districts": districts})


def get_mandis(request):
    state = request.GET.get("state")
    district = request.GET.get("district")

    mandis = df[
        (df["STATE"] == state) &
        (df["District Name"] == district)
    ]["Market Name"].dropna().unique().tolist()

    return JsonResponse({"mandis": mandis})


def get_commodities(request):
    state = request.GET.get("state")
    district = request.GET.get("district")
    mandi = request.GET.get("mandi")

    commodities = df[
        (df["STATE"] == state) &
        (df["District Name"] == district) &
        (df["Market Name"] == mandi)
    ]["Commodity"].dropna().unique().tolist()

    return JsonResponse({"commodities": commodities})


def predict_price(state, district, mandi, commodity):
    filtered = df[
        (df["STATE"] == state) &
        (df["District Name"] == district) &
        (df["Market Name"] == mandi) &
        (df["Commodity"] == commodity)
    ]

    if filtered.empty:
        return None, None, None

    row = filtered.iloc[-1]
    min_p = row["Min_Price"]
    max_p = row["Max_Price"]

    sample = pd.DataFrame({
        "STATE": [state],
        "District Name": [district],
        "Market Name": [mandi],
        "Commodity": [commodity],
        "Min_Price": [min_p],
        "Max_Price": [max_p]
    })

    pred = model.predict(sample)[0]
    return pred, min_p, max_p

@login_required(login_url='/login/')
def crop_price(request):
    prediction = None
    min_price = None
    max_price = None
    error_message = None

    df_states = df["STATE"].dropna().unique().tolist()

    if request.method == "POST":
        state = request.POST.get("state")
        district = request.POST.get("district")
        mandi = request.POST.get("mandi")
        commodity = request.POST.get("commodity")

        pred, min_p, max_p = predict_price(state, district, mandi, commodity)

        if pred is None:
            error_message = "No matching data found. Please check your inputs."
        else:
            prediction = round(pred,2)
            min_price = min_p
            max_price = max_p

    return render(request, "html/crop_price.html", {
        "prediction": prediction,
        "min_price": min_price,
        "max_price": max_price,
        "error_message": error_message,
        "df_states": df_states,
    })
