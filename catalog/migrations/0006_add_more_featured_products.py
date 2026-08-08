from django.db import migrations


def create_more_products(apps, schema_editor):
    Category = apps.get_model('catalog', 'Category')
    Product = apps.get_model('catalog', 'Product')

    products = [
        {
            'name': 'Keten Gömlek Elbise',
            'slug': 'keten-gomlek-elbise',
            'category_slug': 'platya',
            'description': 'Rahat kesimli, günlük kullanıma uygun hafif keten gömlek elbise.',
            'price': '229.00',
        },
        {
            'name': 'İpek Fular',
            'slug': 'ipek-fular',
            'category_slug': 'shali',
            'description': 'Her görünüme zarif bir dokunuş katan yumuşak ipek fular.',
            'price': '99.00',
        },
        {
            'name': 'Hasır Omuz Çantası',
            'slug': 'hasir-omuz-cantasi',
            'category_slug': 'sumki',
            'description': 'Yaz kombinleri için doğal dokulu, kullanışlı omuz çantası.',
            'price': '159.00',
        },
        {
            'name': 'Pamuklu Bluz',
            'slug': 'pamuklu-bluz',
            'category_slug': 'bluzki',
            'description': 'Nefes alan pamuklu kumaştan, sade ve zarif günlük bluz.',
            'price': '139.00',
        },
    ]

    for item in products:
        category = Category.objects.filter(slug=item['category_slug']).first()
        if category is None:
            continue

        Product.objects.update_or_create(
            slug=item['slug'],
            defaults={
                'name': item['name'],
                'category': category,
                'description': item['description'],
                'price': item['price'],
                'is_featured': True,
            },
        )


def remove_more_products(apps, schema_editor):
    Product = apps.get_model('catalog', 'Product')
    Product.objects.filter(
        slug__in=[
            'keten-gomlek-elbise',
            'ipek-fular',
            'hasir-omuz-cantasi',
            'pamuklu-bluz',
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_mark_featured_products'),
    ]

    operations = [
        migrations.RunPython(create_more_products, remove_more_products),
    ]
