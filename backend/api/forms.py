from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory

from .models import MenuCategory, MenuItem, MenuItemVariant, Restaurant


class OwnerUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("email",)


class RestaurantSettingsForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = (
            "address",
            "contact_email",
            "contact_phone",
            "opening_hours_text_en",
            "opening_hours_text_cs",
        )
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
            "opening_hours_text_en": forms.Textarea(attrs={"rows": 4}),
            "opening_hours_text_cs": forms.Textarea(attrs={"rows": 4}),
        }


class MenuCategoryForm(forms.ModelForm):
    class Meta:
        model = MenuCategory
        fields = ("name", "name_alternative")


class MenuItemForm(forms.ModelForm):
    new_category_name = forms.CharField(required=False, label="New category")
    new_category_name_alternative = forms.CharField(required=False, label="New category Czech name")

    class Meta:
        model = MenuItem
        fields = (
            "category",
            "new_category_name",
            "new_category_name_alternative",
            "name",
            "name_alternative",
            "description",
            "description_alternative",
            "price",
            "photo",
            "sort_order",
            "is_active",
            "is_featured",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "description_alternative": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, restaurant=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.restaurant = restaurant
        self.fields["category"].queryset = MenuCategory.objects.filter(restaurant=restaurant).order_by("name")
        self.fields["category"].required = False

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get("category") and not cleaned.get("new_category_name"):
            raise forms.ValidationError("Choose a category or create a new one.")
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        new_category_name = self.cleaned_data.get("new_category_name")
        if new_category_name:
            category, _ = MenuCategory.objects.get_or_create(
                restaurant=self.restaurant,
                name=new_category_name,
                defaults={"name_alternative": self.cleaned_data.get("new_category_name_alternative", "")},
            )
            if self.cleaned_data.get("new_category_name_alternative") and not category.name_alternative:
                category.name_alternative = self.cleaned_data["new_category_name_alternative"]
                category.save(update_fields=["name_alternative"])
            instance.category = category
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class MenuItemVariantForm(forms.ModelForm):
    class Meta:
        model = MenuItemVariant
        fields = ("name", "price", "sort_order")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

    def has_changed(self):
        if not self.data:
            return super().has_changed()
        prefix = self.prefix
        raw_name = self.data.get(f"{prefix}-name", "")
        raw_price = self.data.get(f"{prefix}-price", "")
        raw_sort_order = self.data.get(f"{prefix}-sort_order", "")
        raw_delete = self.data.get(f"{prefix}-DELETE", "")
        if not any([raw_name, raw_price, raw_sort_order, raw_delete]):
            return False
        return super().has_changed()

    def clean(self):
        cleaned = super().clean()
        if self.cleaned_data.get("DELETE"):
            return cleaned
        has_name = bool(cleaned.get("name"))
        has_price = cleaned.get("price") is not None
        has_sort_order = cleaned.get("sort_order") is not None
        if any([has_name, has_price, has_sort_order]) and not all([has_name, has_price]):
            raise forms.ValidationError("Variant name and price are required together.")
        if has_name and cleaned.get("sort_order") is None:
            cleaned["sort_order"] = 0
        return cleaned


MenuItemVariantFormSet = inlineformset_factory(
    MenuItem,
    MenuItemVariant,
    form=MenuItemVariantForm,
    fields=("name", "price", "sort_order"),
    extra=1,
    can_delete=True,
)
