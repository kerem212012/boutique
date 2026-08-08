from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_unique_product_per_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='selected_color',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='selected_size',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.RemoveConstraint(
            model_name='cartitem',
            name='unique_product_per_cart',
        ),
        migrations.AddConstraint(
            model_name='cartitem',
            constraint=models.UniqueConstraint(
                fields=('cart', 'product', 'selected_size', 'selected_color'),
                name='unique_variant_per_cart',
            ),
        ),
    ]