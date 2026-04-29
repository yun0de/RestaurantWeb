# api/urls.py
from django.urls import path,include
from . import views
from . import owner_views

urlpatterns = [
    path("", views.home, name="home"),      # optional if you route home elsewhere
    path("login/", owner_views.OwnerLoginView.as_view(), name="login"),
    path("logout/", owner_views.OwnerLogoutView.as_view(), name="logout"),
    path("menu/", views.menu_page, name="menu"),
    path("owner/", owner_views.owner_dashboard, name="owner_dashboard"),
    path("owner/forbidden/", owner_views.owner_forbidden, name="owner_forbidden"),
    path("owner/menu/", owner_views.owner_menu_list, name="owner_menu"),
    path("owner/menu/new/", owner_views.owner_menu_create, name="owner_menu_create"),
    path("owner/menu/<int:item_id>/edit/", owner_views.owner_menu_edit, name="owner_menu_edit"),
    path("owner/menu/<int:item_id>/delete/", owner_views.owner_menu_delete, name="owner_menu_delete"),
    path("owner/menu/<int:item_id>/toggle-active/", owner_views.owner_menu_toggle_active, name="owner_menu_toggle_active"),
    path("owner/account/", owner_views.owner_account, name="owner_account"),
    path("owner/password/", owner_views.OwnerPasswordChangeView.as_view(), name="owner_password"),
    path("owner/users/new/", owner_views.owner_user_create, name="owner_user_create"),
    path("reservations/", views.reservations, name="reservations"),
]
