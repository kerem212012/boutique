from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Create sample categories and products for the boutique site.'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample categories and products...')

        categories = [
            {
                'name_tr': 'Elbiseler',
                'name_en': 'Dresses',
                'slug': 'dresses',
                'description_tr': 'Şık ve rahat elbiselerimizle yaz stilinizi tamamlayın.',
                'description_en': 'Complete your summer wardrobe with our stylish and comfortable dresses.',
            },
            {
                'name_tr': 'Çantalar',
                'name_en': 'Bags',
                'slug': 'bags',
                'description_tr': 'Günlük kullanıma uygun, şık çanta seçenekleri.',
                'description_en': 'Chic bag options perfect for everyday use.',
            },
            {
                'name_tr': 'Aksesuarlar',
                'name_en': 'Accessories',
                'slug': 'accessories',
                'description_tr': 'Tarzınızı tamamlayacak aksesuarlar.',
                'description_en': 'Accessories that complete your look.',
            },
        ]

        for category_data in categories:
            Category.objects.update_or_create(
                slug=category_data['slug'],
                defaults=category_data,
            )

        category_map = {category.slug: category for category in Category.objects.all()}

        products = [
            {
                'name_tr': 'Keten Yaz Elbisesi',
                'name_en': 'Linen Summer Dress',
                'slug': 'linen-summer-dress',
                'category': category_map['dresses'],
                'description_tr': 'Hafif ve nefes alan keten elbise.',
                'description_en': 'Lightweight linen dress with breathable fabric.',
                'price': '129.99',
                'sizes': ['S', 'M', 'L'],
                'colors': ['Bej', 'Beyaz'],
                'colors_en': ['Beige', 'White'],
                'is_featured': True,
            },
            {
                'name_tr': 'Hasır Omuz Çantası',
                'name_en': 'Woven Shoulder Bag',
                'slug': 'woven-shoulder-bag',
                'category': category_map['bags'],
                'description_tr': 'Günlük kullanıma uygun, doğal dokulu çanta.',
                'description_en': 'Natural textured bag perfect for everyday wear.',
                'price': '89.50',
                'sizes': [],
                'colors': ['Bej', 'Kahverengi'],
                'colors_en': ['Beige', 'Brown'],
            },
            {
                'name_tr': 'İpek Fular',
                'name_en': 'Silk Scarf',
                'slug': 'silk-scarf',
                'category': category_map['accessories'],
                'description_tr': 'İpeksi dokusu ve zarif deseni ile şık bir fular.',
                'description_en': 'Elegant silk scarf with a luxurious feel.',
                'price': '49.00',
                'sizes': [],
                'colors': ['Mavi', 'Pembe'],
                'colors_en': ['Blue', 'Pink'],
            },
        ]

        for product_data in products:
            Product.objects.update_or_create(
                slug=product_data['slug'],
                defaults=product_data,
            )

        self.stdout.write(self.style.SUCCESS('Sample products and categories created.'))
