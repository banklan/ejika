# Generated by Django 3.0.7 on 2020-07-07 10:28

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0017_auto_20200705_1319'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(blank=True, max_length=150, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('text', models.TextField(max_length=400)),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=75, size=[300, 220], upload_to='images/testimonials')),
                ('published', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
