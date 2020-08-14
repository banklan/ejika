# Generated by Django 3.0.7 on 2020-07-01 08:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0013_auto_20200625_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_service', to='services.Service'),
        ),
    ]
