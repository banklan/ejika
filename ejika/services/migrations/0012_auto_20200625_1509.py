# Generated by Django 3.0.7 on 2020-06-25 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0011_auto_20200625_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='image',
            field=models.ImageField(blank=True, default='images/portfolio/no-image.png', upload_to='images/portfolio'),
        ),
    ]