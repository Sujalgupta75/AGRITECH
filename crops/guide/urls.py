from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='guide_home'),
    path('home/', views.home, name='home'),
    path('guide/', views.guide, name='guide'),
]