# Generated by Django 3.0.7 on 2020-07-01 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0014_auto_20200701_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.Service'),
        ),
    ]
