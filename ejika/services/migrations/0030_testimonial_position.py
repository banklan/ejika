# Generated by Django 3.0.7 on 2020-07-27 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0029_auto_20200725_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonial',
            name='position',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
