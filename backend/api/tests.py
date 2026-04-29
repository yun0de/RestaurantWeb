from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import MenuCategory, MenuItem, Restaurant
from .owner_access import OWNER_GROUP_NAME
from .site_context import get_or_create_primary_restaurant


class OwnerPanelTests(TestCase):
    def setUp(self):
        Restaurant.objects.all().delete()
        self.restaurant = Restaurant.objects.create(
            name="Boong Restaurant",
            address="Test Address",
            contact_email="hello@example.com",
            contact_phone="+420 111 222 333",
            opening_hours_text_en="Open EN",
            opening_hours_text_cs="Open CS",
        )
        self.category = MenuCategory.objects.create(restaurant=self.restaurant, name="Soup")
        self.active_item = MenuItem.objects.create(
            category=self.category,
            name="Visible Pho",
            description="Shown",
            price=195,
            is_active=True,
            is_featured=True,
        )
        self.hidden_item = MenuItem.objects.create(
            category=self.category,
            name="Hidden Pho",
            description="Hidden",
            price=205,
            is_active=False,
            is_featured=True,
        )
        self.owner_group, _ = Group.objects.get_or_create(name=OWNER_GROUP_NAME)
        User = get_user_model()
        self.superuser = User.objects.create_superuser("admin", "admin@example.com", "AdminPass12345!")
        self.owner = User.objects.create_user("owner", "owner@example.com", "OwnerPass12345!")
        self.owner.groups.add(self.owner_group)
        self.regular = User.objects.create_user("regular", "regular@example.com", "RegularPass12345!")

    def test_owner_routes_require_owner_role(self):
        response = self.client.get(reverse("owner_dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

        self.client.force_login(self.regular)
        response = self.client.get(reverse("owner_dashboard"))
        self.assertEqual(response.status_code, 403)

        self.client.force_login(self.owner)
        response = self.client.get(reverse("owner_dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_admin_nav_link_only_shows_after_login(self):
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, reverse("owner_dashboard"))
        self.assertNotContains(response, "Admin")

        self.client.force_login(self.owner)
        response = self.client.get(reverse("home"))
        self.assertContains(response, reverse("owner_dashboard"))
        self.assertContains(response, "Admin")

    def test_owner_does_not_access_django_admin_but_superuser_does(self):
        self.client.force_login(self.owner)
        owner_response = self.client.get(reverse("admin:index"))
        self.assertNotEqual(owner_response.status_code, 200)

        self.client.force_login(self.superuser)
        admin_response = self.client.get(reverse("admin:index"))
        self.assertEqual(admin_response.status_code, 200)

    def test_superuser_creates_owner_account(self):
        self.client.force_login(self.superuser)
        response = self.client.post(
            reverse("owner_user_create"),
            {
                "username": "newowner",
                "email": "newowner@example.com",
                "password1": "NewOwnerPass12345!",
                "password2": "NewOwnerPass12345!",
            },
        )
        self.assertEqual(response.status_code, 302)
        user = get_user_model().objects.get(username="newowner")
        self.assertFalse(user.is_staff)
        self.assertTrue(user.groups.filter(name=OWNER_GROUP_NAME).exists())

        self.client.force_login(self.owner)
        denied_response = self.client.get(reverse("owner_user_create"))
        self.assertEqual(denied_response.status_code, 302)

    def test_public_pages_only_show_active_items(self):
        home_response = self.client.get(reverse("home"))
        self.assertContains(home_response, "Visible Pho")
        self.assertNotContains(home_response, "Hidden Pho")

        menu_response = self.client.get(reverse("menu"))
        self.assertContains(menu_response, "Visible Pho")
        self.assertNotContains(menu_response, "Hidden Pho")

    def test_inactive_signature_does_not_show_on_homepage(self):
        self.active_item.is_active = False
        self.active_item.save(update_fields=["is_active"])
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, "Visible Pho")

    def test_restaurant_settings_render_public_contact_details(self):
        response = self.client.get(reverse("home"), HTTP_ACCEPT_LANGUAGE="en")
        self.assertContains(response, "Test Address")
        self.assertContains(response, "hello@example.com")
        self.assertContains(response, "+420 111 222 333")
        self.assertContains(response, "Open EN")

        response = self.client.get(reverse("home"), HTTP_ACCEPT_LANGUAGE="cs")
        self.assertContains(response, "Open CS")

    def test_primary_restaurant_prefers_populated_settings(self):
        blank_restaurant = Restaurant.objects.create(name="Blank")

        restaurant = get_or_create_primary_restaurant()

        self.assertEqual(restaurant.id, self.restaurant.id)
        self.assertEqual(blank_restaurant.address, "")

    def test_owner_can_update_restaurant_settings(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("owner_dashboard"),
            {
                "address": "New Address",
                "contact_email": "new@example.com",
                "contact_phone": "+420 999 888 777",
                "opening_hours_text_en": "New EN hours",
                "opening_hours_text_cs": "New CS hours",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.address, "New Address")
        self.assertEqual(self.restaurant.contact_email, "new@example.com")
        self.assertEqual(self.restaurant.contact_phone, "+420 999 888 777")

    def test_owner_menu_crud_and_active_toggle(self):
        self.client.force_login(self.owner)
        upload = SimpleUploadedFile(
            "dish.gif",
            b"GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00\xff\xff\xff,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;",
            content_type="image/gif",
        )
        response = self.client.post(
            reverse("owner_menu_create"),
            {
                "category": self.category.id,
                "new_category_name": "",
                "new_category_name_alternative": "",
                "name": "Owner Dish",
                "name_alternative": "Owner jidlo",
                "description": "Owner description",
                "description_alternative": "Owner popis",
                "price": "199.00",
                "photo": upload,
                "sort_order": "10",
                "is_active": "on",
                "is_featured": "on",
                "variants-TOTAL_FORMS": "1",
                "variants-INITIAL_FORMS": "0",
                "variants-MIN_NUM_FORMS": "0",
                "variants-MAX_NUM_FORMS": "1000",
                "variants-0-name": "",
                "variants-0-price": "",
                "variants-0-sort_order": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        item = MenuItem.objects.get(name="Owner Dish")
        self.assertTrue(item.is_active)
        self.assertTrue(item.is_featured)

        response = self.client.post(reverse("owner_menu_toggle_active", args=[item.id]))
        self.assertEqual(response.status_code, 302)
        item.refresh_from_db()
        self.assertFalse(item.is_active)

        response = self.client.post(reverse("owner_menu_delete", args=[item.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(MenuItem.objects.filter(id=item.id).exists())
