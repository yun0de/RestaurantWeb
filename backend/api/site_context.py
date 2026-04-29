from django.utils.translation import get_language

from .models import Restaurant


DEFAULT_ADDRESS = "Budečská 816/4\n120 00 Praha 2, Vinohrady\nCzech Republic"
DEFAULT_EMAIL = "manhthanhdat94@gmail.com"
DEFAULT_PHONE = "+420 777 170 468"
DEFAULT_OPENING_HOURS_EN = "Mon - Fri 11:00 - 22:30\nSaturday 11:00 - 22:30\nSunday 11:00 - 22:30"
DEFAULT_OPENING_HOURS_CS = "Po - Pá 11:00 - 22:30\nSobota 11:00 - 22:30\nNeděle 11:00 - 22:30"
DEFAULT_OPENING_HOURS = DEFAULT_OPENING_HOURS_EN


RESTAURANT_DEFAULTS = {
    "address": DEFAULT_ADDRESS,
    "contact_email": DEFAULT_EMAIL,
    "contact_phone": DEFAULT_PHONE,
    "opening_hours_text_en": DEFAULT_OPENING_HOURS_EN,
    "opening_hours_text_cs": DEFAULT_OPENING_HOURS_CS,
}


def get_primary_restaurant():
    return (
        Restaurant.objects
        .exclude(address="")
        .exclude(contact_email="")
        .exclude(contact_phone="")
        .order_by("id")
        .first()
        or Restaurant.objects.order_by("id").first()
    )


def fill_restaurant_defaults(restaurant):
    changed_fields = []
    for field, value in RESTAURANT_DEFAULTS.items():
        if not getattr(restaurant, field):
            setattr(restaurant, field, value)
            changed_fields.append(field)

    if changed_fields:
        restaurant.save(update_fields=changed_fields)

    return restaurant


def get_or_create_primary_restaurant():
    restaurant = get_primary_restaurant()
    if restaurant:
        return fill_restaurant_defaults(restaurant)
    return Restaurant.objects.create(name="Boong Restaurant", **RESTAURANT_DEFAULTS)


def phone_href(phone):
    return "".join(char for char in phone if char.isdigit() or char == "+")


def restaurant_settings(request):
    restaurant = get_primary_restaurant()
    language = get_language()

    address = restaurant.address if restaurant and restaurant.address else DEFAULT_ADDRESS
    email = restaurant.contact_email if restaurant and restaurant.contact_email else DEFAULT_EMAIL
    phone = restaurant.contact_phone if restaurant and restaurant.contact_phone else DEFAULT_PHONE

    opening_hours = DEFAULT_OPENING_HOURS
    if restaurant:
        primary = restaurant.opening_hours_text_cs if language == "cs" else restaurant.opening_hours_text_en
        fallback = restaurant.opening_hours_text_en if language == "cs" else restaurant.opening_hours_text_cs
        opening_hours = primary or fallback or DEFAULT_OPENING_HOURS

    return {
        "site_restaurant": restaurant,
        "site_address": address,
        "site_contact_email": email,
        "site_contact_phone": phone,
        "site_contact_phone_href": phone_href(phone),
        "site_opening_hours": opening_hours,
    }
