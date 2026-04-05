from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("", login_required(views.home, login_url='/login/'), name="soil_health_home"),
    path('soil_health/', login_required(views.soil_health, login_url='/login/'), name='soil_health'),
]
