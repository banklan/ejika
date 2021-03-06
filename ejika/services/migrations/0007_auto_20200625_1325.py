# Generated by Django 3.0.7 on 2020-06-25 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_auto_20200622_2257'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='portfolio',
            options={'ordering': ['-created']},
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='description',
            field=models.TextField(max_length=400),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service', to='services.Service'),
        ),
    ]
