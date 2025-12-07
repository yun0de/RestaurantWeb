# api/urls.py
from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.home, name="home"),      # optional if you route home elsewhere
    path("menu/", views.menu, name="menu"), # <-- this creates the 'menu' name
    path("reservations/", views.reservations, name="reservations"),
]
