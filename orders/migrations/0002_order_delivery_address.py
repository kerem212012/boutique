from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_address',
            field=models.TextField(blank=True),
        ),
    ]
