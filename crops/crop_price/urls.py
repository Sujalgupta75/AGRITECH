from django.urls import path
from .views import crop_price, get_districts, get_mandis, get_commodities
from . import views

urlpatterns = [
    path('', views.home, name='fertilizer_home'),
    path('home/', views.home, name='home'),
    path('crop_price/', views.crop_price, name='crop_price'),
    path("api/districts/", get_districts, name="get_districts"),
    path("api/mandis/", get_mandis, name="get_mandis"),
    path("api/commodities/", get_commodities, name="get_commodities"),
]