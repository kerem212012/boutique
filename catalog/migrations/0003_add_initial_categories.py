from django.db import migrations


def create_categories(apps, schema_editor):
    Category = apps.get_model('catalog', 'Category')
    categories = [
        ('платья', 'platya'),
        ('блузки', 'bluzki'),
        ('штаны', 'shtany'),
        ('шорты', 'shorty'),
        ('шали', 'shali'),
        ('юбки', 'yubki'),
        ('сумки', 'sumki'),
    ]
    for name, slug in categories:
        Category.objects.get_or_create(name=name, slug=slug)


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_category_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.RunPython(create_categories),
    ]
