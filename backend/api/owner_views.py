from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST

from .forms import (
    AccountUpdateForm,
    MenuItemForm,
    MenuItemVariantFormSet,
    OwnerUserCreationForm,
    RestaurantSettingsForm,
)
from .models import MenuItem, Restaurant
from .owner_access import OWNER_GROUP_NAME, is_owner_user, owner_required
from .site_context import get_or_create_primary_restaurant


def superuser_required(view_func):
    return user_passes_test(lambda user: user.is_active and user.is_superuser, login_url="login")(view_func)


class OwnerLoginView(LoginView):
    template_name = "owner/login.html"
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        if is_owner_user(self.request.user):
            return reverse_lazy("owner_dashboard")
        return reverse_lazy("owner_forbidden")


class OwnerLogoutView(LogoutView):
    next_page = "home"


class OwnerPasswordChangeView(PasswordChangeView):
    template_name = "owner/password.html"
    success_url = reverse_lazy("owner_account")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{reverse('login')}?next={request.get_full_path()}")
        if not is_owner_user(request.user):
            return redirect("owner_forbidden")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Password updated.")
        return super().form_valid(form)


@login_required
def owner_forbidden(request):
    return render(request, "owner/forbidden.html", status=403)


@owner_required
def owner_dashboard(request):
    restaurant = get_or_create_primary_restaurant()
    if request.method == "POST":
        form = RestaurantSettingsForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, "Restaurant settings saved.")
            return redirect("owner_dashboard")
    else:
        form = RestaurantSettingsForm(instance=restaurant)

    featured_count = MenuItem.objects.filter(is_active=True, is_featured=True).count()
    inactive_count = MenuItem.objects.filter(is_active=False).count()
    return render(
        request,
        "owner/dashboard.html",
        {
            "form": form,
            "featured_count": featured_count,
            "inactive_count": inactive_count,
        },
    )


@owner_required
def owner_menu_list(request):
    items = MenuItem.objects.select_related("category").prefetch_related("variants").order_by(
        "category__name", "sort_order", "id"
    )
    return render(request, "owner/menu_list.html", {"items": items})


@owner_required
def owner_menu_create(request):
    restaurant = get_or_create_primary_restaurant()
    item = MenuItem()
    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES, instance=item, restaurant=restaurant)
        formset = MenuItemVariantFormSet(request.POST, instance=item)
        if form.is_valid() and formset.is_valid():
            item = form.save()
            formset.instance = item
            formset.save()
            messages.success(request, "Menu item created.")
            return redirect("owner_menu")
    else:
        form = MenuItemForm(instance=item, restaurant=restaurant)
        formset = MenuItemVariantFormSet(instance=item)
    return render(request, "owner/menu_form.html", {"form": form, "formset": formset, "item": item})


@owner_required
def owner_menu_edit(request, item_id):
    restaurant = get_or_create_primary_restaurant()
    item = get_object_or_404(MenuItem, pk=item_id)
    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES, instance=item, restaurant=restaurant)
        formset = MenuItemVariantFormSet(request.POST, instance=item)
        if form.is_valid() and formset.is_valid():
            item = form.save()
            formset.save()
            messages.success(request, "Menu item saved.")
            return redirect("owner_menu")
    else:
        form = MenuItemForm(instance=item, restaurant=restaurant)
        formset = MenuItemVariantFormSet(instance=item)
    return render(request, "owner/menu_form.html", {"form": form, "formset": formset, "item": item})


@owner_required
def owner_menu_delete(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Menu item deleted.")
        return redirect("owner_menu")
    return render(request, "owner/menu_confirm_delete.html", {"item": item})


@owner_required
@require_POST
def owner_menu_toggle_active(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id)
    item.is_active = not item.is_active
    item.save(update_fields=["is_active"])
    return redirect("owner_menu")


@owner_required
def owner_account(request):
    if request.method == "POST":
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account updated.")
            return redirect("owner_account")
    else:
        form = AccountUpdateForm(instance=request.user)
    return render(request, "owner/account.html", {"form": form})


@superuser_required
def owner_user_create(request):
    if request.method == "POST":
        form = OwnerUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False
            user.save()
            owner_group, _ = Group.objects.get_or_create(name=OWNER_GROUP_NAME)
            user.groups.add(owner_group)
            messages.success(request, "Owner account created.")
            return redirect("owner_dashboard")
    else:
        form = OwnerUserCreationForm()
    return render(request, "owner/user_form.html", {"form": form})
