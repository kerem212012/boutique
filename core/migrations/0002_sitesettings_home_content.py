from django.db import migrations, models


def replace_old_default_tagline(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    SiteSettings.objects.filter(tagline='Modern boutique experience').update(
        tagline='Doğallığın ve şıklığın buluştuğu adres...'
    )


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='tagline',
            field=models.CharField(default='Doğallığın ve şıklığın buluştuğu adres...', max_length=200),
        ),
        migrations.RunPython(replace_old_default_tagline, migrations.RunPython.noop),
        migrations.AddField(
            model_name='sitesettings',
            name='about_text_en',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='bottom_image',
            field=models.ImageField(blank=True, null=True, upload_to='site/'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='hero_image',
            field=models.ImageField(blank=True, null=True, upload_to='site/'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='location',
            field=models.CharField(default='Kalkan, Antalya', max_length=200),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='new_arrivals_image',
            field=models.ImageField(blank=True, null=True, upload_to='site/'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='tagline_en',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
