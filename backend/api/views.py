from django.shortcuts import render, get_object_or_404
from .models import Restaurant, MenuItem

def home(request):
    featured_items = MenuItem.objects.filter(is_featured=True)[:6]

    return render(request, "home.html", {
        "menu_items": featured_items
    })


def reservations(request):
    # simple placeholder reservations page (expand later to handle forms)
    return render(request, "reservations.html")



def menu_page(request):
    items = MenuItem.objects.all().order_by("name")
    return render(request, "menu.html", {
        "items": items
    })
