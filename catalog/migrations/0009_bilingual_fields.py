from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_add_product_options_data'),
    ]

    operations = [
        # Category: rename name/description → _tr variants, add _en variants
        migrations.RenameField(
            model_name='category',
            old_name='name',
            new_name='name_tr',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='description',
            new_name='description_tr',
        ),
        migrations.AddField(
            model_name='category',
            name='name_en',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='category',
            name='description_en',
            field=models.TextField(blank=True),
        ),
        # Product: rename name/description → _tr variants, add _en variants
        migrations.RenameField(
            model_name='product',
            old_name='name',
            new_name='name_tr',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='description',
            new_name='description_tr',
        ),
        migrations.AddField(
            model_name='product',
            name='name_en',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='product',
            name='description_en',
            field=models.TextField(blank=True),
        ),
    ]
