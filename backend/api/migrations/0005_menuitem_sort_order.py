from django.db import migrations, models


def backfill_menu_item_sort_order(apps, schema_editor):
    MenuItem = apps.get_model("api", "MenuItem")

    for category_id in (
        MenuItem.objects.order_by().values_list("category_id", flat=True).distinct()
    ):
        items = MenuItem.objects.filter(category_id=category_id).order_by("id")
        for position, item in enumerate(items, start=1):
            item.sort_order = position
            item.save(update_fields=["sort_order"])


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_menuitemvariant_alter_menuitem_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="menuitem",
            name="sort_order",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.RunPython(
            backfill_menu_item_sort_order,
            migrations.RunPython.noop,
        ),
    ]
