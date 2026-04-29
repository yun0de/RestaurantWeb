from django.contrib import admin
from .models import Restaurant, MenuCategory, MenuItem, MenuItemVariant, Reservation

admin.site.has_permission = lambda request: request.user.is_active and request.user.is_superuser

admin.site.register(Restaurant)
admin.site.register(MenuCategory)
admin.site.register(Reservation)

class MenuItemVariantInline(admin.TabularInline):
    model = MenuItemVariant
    extra = 1
    fields = ("name", "price", "sort_order")
    ordering = ("sort_order", "id")


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "sort_order", "price_summary", "is_active", "is_featured")
    list_filter = ("category", "is_active", "is_featured")
    search_fields = ("name", "description", "variants__name")
    list_editable = ("sort_order",)
    ordering = ("category", "sort_order", "id")
    inlines = [MenuItemVariantInline]


@admin.register(MenuItemVariant)
class MenuItemVariantAdmin(admin.ModelAdmin):
    list_display = ("menu_item", "name", "price", "sort_order")
    list_filter = ("menu_item__category",)
    search_fields = ("menu_item__name", "name")
