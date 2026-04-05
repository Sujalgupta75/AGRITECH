from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd
import joblib
import numpy as np
# Create your views here.

@login_required(login_url='/login/')
def home(request):
    return render(request, 'html/home.html')

model = joblib.load("fertilizer_model.pkl")

@login_required(login_url='/login/')
def fertilizer(request):
    prediction = None

    if request.method == "POST":

        data = {
            "Nitrogen": [float(request.POST.get("Nitrogen"))],
            "Phosphorous": [float(request.POST.get("Phosphorous"))],
            "Potassium": [float(request.POST.get("Potassium"))],
            "Temperature": [float(request.POST.get("Temperature"))],
            "Humidity": [float(request.POST.get("Humidity"))],
            "Ph": [float(request.POST.get("Ph"))],
            "Moisture": [float(request.POST.get("Moisture"))],

            # These MUST remain strings because OneHotEncoder expects strings
            "Soil_Type": [request.POST.get("Soil_Type")],
            "Crop_Type": [request.POST.get("Crop_Type")]
        }

        df = pd.DataFrame(data)

        prediction = model.predict(df)[0]

    return render(request, "html/fertilizer.html", {"prediction": prediction})