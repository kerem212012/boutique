from django.db import migrations, models


def merge_duplicate_cart_items(apps, schema_editor):
    CartItem = apps.get_model('cart', 'CartItem')
    from django.db.models import Count, Sum

    duplicates = (
        CartItem.objects.values('cart_id', 'product_id')
        .annotate(item_count=Count('id'))
        .filter(item_count__gt=1)
    )
    for duplicate in duplicates:
        items = CartItem.objects.filter(
            cart_id=duplicate['cart_id'],
            product_id=duplicate['product_id'],
        ).order_by('id')
        first_item = items.first()
        first_item.quantity = items.aggregate(total=Sum('quantity'))['total']
        first_item.save(update_fields=('quantity',))
        items.exclude(id=first_item.id).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(merge_duplicate_cart_items, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name='cartitem',
            constraint=models.UniqueConstraint(
                fields=('cart', 'product'),
                name='unique_product_per_cart',
            ),
        ),
    ]