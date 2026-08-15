from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('catalog', '0002_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_new',
            field=models.BooleanField(default=False),
        ),
    ]
