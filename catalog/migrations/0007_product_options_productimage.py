from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_add_more_featured_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='colors',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/gallery/')),
                ('alt_text', models.CharField(blank=True, max_length=200)),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='gallery', to='catalog.product')),
            ],
            options={'ordering': ('sort_order', 'id')},
        ),
    ]