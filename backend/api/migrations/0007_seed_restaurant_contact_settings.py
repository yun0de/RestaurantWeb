from django.db import migrations


DEFAULTS = {
    "address": "Budečská 816/4\n120 00 Praha 2, Vinohrady\nCzech Republic",
    "contact_email": "manhthanhdat94@gmail.com",
    "contact_phone": "+420 777 170 468",
    "opening_hours_text_en": "Mon - Fri 11:00 - 22:30\nSaturday 11:00 - 22:30\nSunday 11:00 - 22:30",
    "opening_hours_text_cs": "Po - Pá 11:00 - 22:30\nSobota 11:00 - 22:30\nNeděle 11:00 - 22:30",
}


def seed_restaurant_settings(apps, schema_editor):
    Restaurant = apps.get_model("api", "Restaurant")
    restaurant = Restaurant.objects.order_by("id").first()
    if restaurant is None:
        Restaurant.objects.create(name="Boong Restaurant", **DEFAULTS)
        return

    changed_fields = []
    for field, value in DEFAULTS.items():
        if not getattr(restaurant, field):
            setattr(restaurant, field, value)
            changed_fields.append(field)

    if changed_fields:
        restaurant.save(update_fields=changed_fields)


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_alter_menuitem_options_menuitem_is_active_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_restaurant_settings, migrations.RunPython.noop),
    ]
