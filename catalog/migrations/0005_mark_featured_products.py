from django.db import migrations


def mark_featured_products(apps, schema_editor):
    Product = apps.get_model('catalog', 'Product')
    featured_slugs = [
        'bluzka-iz-shelkovogo-trikotazha',
        'lnyanye-shirokie-shtany',
        'shorty-s-zavishhennoj-taliey',
        'shal-shelkovaya-tsvetochnaya',
        'yubka-midi-plissirovannaya',
        'sumka-tot-iz-lna',
    ]
    Product.objects.filter(slug__in=featured_slugs).update(is_featured=True)


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_add_initial_products'),
    ]

    operations = [
        migrations.RunPython(mark_featured_products),
    ]
