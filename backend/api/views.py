from django.shortcuts import render, get_object_or_404
from .models import Restaurant, MenuItem

def home(request):
    # choose first restaurant (or None)
    restaurant = Restaurant.objects.first()
    if restaurant:
        # get items for that restaurant via the category relation
        menu_items = MenuItem.objects.filter(category__restaurant=restaurant).order_by('name')[:6]
    else:
        menu_items = MenuItem.objects.all().order_by('name')[:6]

    return render(request, 'home.html', {
        'restaurants': Restaurant.objects.all(),
        'menu_items': menu_items,
    })


def menu(request):
    # replace "menu.html" with your actual template for the menu
    return render(request, "menu.html")


def reservations(request):
    # simple placeholder reservations page (expand later to handle forms)
    return render(request, "reservations.html")

