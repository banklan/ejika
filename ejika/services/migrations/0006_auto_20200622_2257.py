# Generated by Django 3.0.7 on 2020-06-22 21:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_auto_20200622_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='portfolio',
            name='description',
            field=models.TextField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='portfolio',
            name='image',
            field=models.ImageField(blank=True, default='images/portfolio/no-image.png', null=True, upload_to='images/portfolio'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='service',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='services.Service'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='portfolio',
            name='slug',
            field=models.SlugField(default=1, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='portfolio',
            name='title',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
