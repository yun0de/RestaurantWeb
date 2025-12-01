from django.shortcuts import render
from .models import Restaurant, MenuItem

def home(request):
    restaurants = Restaurant.objects.all()
    # Example: show first restaurant's menu items if available
    menu_items = MenuItem.objects.all()[:6]
    return render(request, 'home.html', {'restaurants': restaurants, 'menu_items': menu_items})
