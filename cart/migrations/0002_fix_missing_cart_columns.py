from django.db import migrations, models
from django.utils import timezone


def forwards(apps, schema_editor):
    Cart = apps.get_model("cart", "Cart")
    connection = schema_editor.connection

    with connection.cursor() as cursor:
        columns = {
            column.name
            for column in connection.introspection.get_table_description(
                cursor, Cart._meta.db_table
            )
        }

        constraints = connection.introspection.get_constraints(
            cursor, Cart._meta.db_table
        )

    if "active" not in columns:
        active_field = models.BooleanField(default=True)
        active_field.set_attributes_from_name("active")
        schema_editor.add_field(Cart, active_field)

    if "created_at" not in columns:
        created_at_field = models.DateTimeField(default=timezone.now)
        created_at_field.set_attributes_from_name("created_at")
        schema_editor.add_field(Cart, created_at_field)

    # If the database already had multiple carts per user, keep the oldest one
    # active and deactivate the rest before the unique constraint is enforced.
    if "active" in columns or "active" in {c.name for c in Cart._meta.fields}:
        for user_id in Cart.objects.values_list("user_id", flat=True).distinct():
            carts = list(Cart.objects.filter(user_id=user_id).order_by("id"))
            if len(carts) > 1:
                for cart in carts[1:]:
                    if cart.active:
                        cart.active = False
                        cart.save(update_fields=["active"])

    if "unique_active_cart_per_user" not in constraints:
        schema_editor.add_constraint(
            Cart,
            models.UniqueConstraint(
                fields=["user"],
                condition=models.Q(active=True),
                name="unique_active_cart_per_user",
            ),
        )


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
