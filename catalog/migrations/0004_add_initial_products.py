from django.db import migrations


def create_products(apps, schema_editor):
    Category = apps.get_model('catalog', 'Category')
    Product = apps.get_model('catalog', 'Product')

    products = [
        {
            'name': 'Льняное платье с воланами',
            'slug': 'lnyanoe-plate-s-volanami',
            'category_slug': 'platy',
            'description': 'Уютное льняное платье с мягкими воланами и романтичным силуэтом.',
            'price': '249.90',
        },
        {
            'name': 'Блузка из шелкового трикотажа',
            'slug': 'bluzka-iz-shelkovogo-trikotazha',
            'category_slug': 'bluzki',
            'description': 'Легкая блузка с нежным блеском и рукавами-буфами.',
            'price': '179.50',
        },
        {
            'name': 'Льняные широкие штаны',
            'slug': 'lnyanye-shirokie-shtany',
            'category_slug': 'shtany',
            'description': 'Свободные брюки из натурального льна для повседневного комфорта.',
            'price': '199.00',
        },
        {
            'name': 'Шорты с завышенной талией',
            'slug': 'shorty-s-zavishhennoj-taliey',
            'category_slug': 'shorty',
            'description': 'Летние шорты на пуговицах с мягкой посадкой и стильным кроем.',
            'price': '149.90',
        },
        {
            'name': 'Шаль шелковая цветочная',
            'slug': 'shal-shelkovaya-tsvetochnaya',
            'category_slug': 'shali',
            'description': 'Нежная шаль с цветочным узором, которая украшает любой образ.',
            'price': '129.00',
        },
        {
            'name': 'Юбка миди плиссированная',
            'slug': 'yubka-midi-plissirovannaya',
            'category_slug': 'yubki',
            'description': 'Плиссированная миди-юбка с легким движением и элегантным силуэтом.',
            'price': '189.90',
        },
        {
            'name': 'Сумка-тоут из льна',
            'slug': 'sumka-tot-iz-lna',
            'category_slug': 'sumki',
            'description': 'Практичная сумка-тоут с плотной ручкой и натуральной текстурой.',
            'price': '219.00',
        },
        {
            'name': 'Летнее платье на тонких бретелях',
            'slug': 'letnee-plate-na-tonkih-bretyelyah',
            'category_slug': 'platy',
            'description': 'Воздушное платье для прогулок по побережью и вечерних встреч.',
            'price': '239.00',
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
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_add_initial_categories'),
    ]

    operations = [
        migrations.RunPython(create_products),
    ]
