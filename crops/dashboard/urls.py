from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='dashboard_home'),
    path('home/', views.home, name='home'),
    path('listcrop/', views.listcrop, name='listcrop'),
    path('get-districts/', views.get_districts, name="get_districts"),
]