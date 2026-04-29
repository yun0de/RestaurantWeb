from django.db import migrations


DEFAULTS = {
    "address": "Budečská 816/4\n120 00 Praha 2, Vinohrady\nCzech Republic",
    "contact_email": "manhthanhdat94@gmail.com",
    "contact_phone": "+420 777 170 468",
    "opening_hours_text_en": "Mon - Fri 11:00 - 22:30\nSaturday 11:00 - 22:30\nSunday 11:00 - 22:30",
    "opening_hours_text_cs": "Po - Pá 11:00 - 22:30\nSobota 11:00 - 22:30\nNeděle 11:00 - 22:30",
}


def fill_existing_restaurant_defaults(apps, schema_editor):
    Restaurant = apps.get_model("api", "Restaurant")

    if not Restaurant.objects.exists():
        Restaurant.objects.create(name="Boong Restaurant", **DEFAULTS)
        return

    for restaurant in Restaurant.objects.all():
        changed_fields = []
        for field, value in DEFAULTS.items():
            if not getattr(restaurant, field):
                setattr(restaurant, field, value)
                changed_fields.append(field)

        if changed_fields:
            restaurant.save(update_fields=changed_fields)


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0007_seed_restaurant_contact_settings"),
    ]

    operations = [
        migrations.RunPython(fill_existing_restaurant_defaults, migrations.RunPython.noop),
    ]
