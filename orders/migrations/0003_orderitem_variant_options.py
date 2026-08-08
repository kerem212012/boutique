from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_order_is_paid_remove_order_note_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='selected_color',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='selected_size',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]