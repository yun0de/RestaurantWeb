from django.contrib import admin
from .models import Restaurant, MenuCategory, MenuItem, Reservation

admin.site.register(Restaurant)
admin.site.register(MenuCategory)
admin.site.register(Reservation)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_featured")
    list_filter = ("is_featured",)
    search_fields = ("name", "description")
