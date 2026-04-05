from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests
from datetime import datetime

@login_required(login_url='/login/')
def home(request):
    return render(request, 'html/home.html')


def weather(request):
    state_districts = {
        "Rajasthan": ["Bharatpur", "Jaipur", "Udaipur"],
        "Uttar Pradesh": ["Noida", "Lucknow", "Varanasi"],
        "Maharashtra": ["Mumbai", "Pune", "Nagpur"],
        "Bihar": ["Patna", "Gaya", "Muzaffarpur"],
    }

    context = {
        'states': state_districts.keys(),
        'state_districts': state_districts,
    }

    if request.method == 'POST':
        state = request.POST.get('state')
        district = request.POST.get('district')

        if not state or not district:
            context['error'] = "Please select both state and district."
            return render(request, 'html/weather.html', context)

        API_KEY = "ce94ea7b998d69e4acc4265575d057ac"
        country_code = "IN"

        # Step 1: Get Latitude and Longitude
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={district},{state},{country_code}&limit=1&appid={API_KEY}"
        geo_response = requests.get(geo_url).json()

        if not geo_response:
            context['error'] = "Location not found. Try another district."
            return render(request, 'html/weather.html', context)

        lat = geo_response[0]['lat']
        lon = geo_response[0]['lon']

        # Step 2: Use the 5-day / 3-hour forecast API instead (working endpoint)
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        forecast_response = requests.get(forecast_url).json()

        if "list" not in forecast_response:
            context['error'] = "Weather data not available for this location."
            return render(request, 'html/weather.html', context)

        # Step 3: Extract useful fields (1 per day)
        daily_data = {}
        for item in forecast_response["list"]:
            date = datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d")
            if date not in daily_data:
                daily_data[date] = {
                    "date": date,
                    "temp": item["main"]["temp"],
                    "feels_like": item["main"]["feels_like"],
                    "humidity": item["main"]["humidity"],
                    "weather": item["weather"][0]["description"].title(),
                }

        context.update({
            "city_name": forecast_response["city"]["name"],
            "forecast": list(daily_data.values())
        })

    return render(request, 'html/weather.html', context)
