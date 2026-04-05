from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd
import joblib
# Create your views here.

@login_required(login_url='/login/')
def home(request):
    return render(request, 'html/home.html')


model = joblib.load("nutrients_model.pkl")

@login_required(login_url='/login/')
def soil_health(request):
    prediction = None

    if request.method == "POST":
        N = float(request.POST["N"])
        P = float(request.POST["P"])
        K = float(request.POST["K"])
        ph = float(request.POST["ph"])
        rainfall = float(request.POST["rainfall"])
        humidity = float(request.POST["humidity"])

        df = pd.DataFrame([{
            "N": N,
            "P": P,
            "K": K,
            "temperature": 25,     # You can remove if dataset doesn't use
            "humidity": humidity,
            "ph": ph,
            "rainfall": rainfall
        }])

        prediction = model.predict(df)[0]


    return render(request, "html/soil_health.html", {"prediction": prediction})