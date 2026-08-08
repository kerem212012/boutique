from django.db import migrations


def add_product_options(apps, schema_editor):
    Product = apps.get_model('catalog', 'Product')
    one_size_slugs = {
        'ipek-fular',
        'hasir-omuz-cantasi',
        'sumka-tot-iz-lna',
        'shal-shelkovaya-tsvetochnaya',
    }

    for product in Product.objects.all():
        if not product.sizes:
            product.sizes = ['One Size'] if product.slug in one_size_slugs else ['S', 'M', 'L']
        if not product.colors:
            product.colors = ['Black', 'White', 'Natural']
        product.save(update_fields=('sizes', 'colors'))


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_product_options_productimage'),
    ]

    operations = [
        migrations.RunPython(add_product_options, migrations.RunPython.noop),
    ]