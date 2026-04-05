from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='fertilizer_home'),
    path('home/', views.home, name='home'),
    path('fertilizer/', views.fertilizer, name='fertilizer'),
]
