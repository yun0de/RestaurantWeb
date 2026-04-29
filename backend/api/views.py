from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
from .models import Restaurant, MenuItem, MenuCategory

def home(request):
    featured_items = (
        MenuItem.objects
        .filter(is_active=True, is_featured=True)
        .prefetch_related("variants")
        .order_by("sort_order", "id")[:6]
    )

    return render(request, "home.html", {
        "menu_items": featured_items
    })


def reservations(request):
    # simple placeholder reservations page (expand later to handle forms)
    return render(request, "reservations.html")



def menu_page(request):
    ordered_items = MenuItem.objects.filter(is_active=True).prefetch_related("variants").order_by("sort_order", "id")
    categories = MenuCategory.objects.prefetch_related(
        Prefetch("items", queryset=ordered_items)
    ).all()
    return render(request, "menu.html", {
        "categories": categories
    })
