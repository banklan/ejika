# Generated by Django 3.0.7 on 2020-07-05 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0015_auto_20200701_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='fb',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='instag',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
    ]