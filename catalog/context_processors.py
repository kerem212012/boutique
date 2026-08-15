from django.utils.translation import get_language

from .models import Category


def nav_categories(request):
    lang = get_language()
    order_field = 'name_en' if lang and lang.startswith('en') else 'name_tr'
    return {
        'nav_categories': Category.objects.order_by(order_field).all(),
    }
