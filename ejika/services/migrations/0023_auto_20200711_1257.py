# Generated by Django 3.0.7 on 2020-07-11 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0022_financeapplication_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnquiryContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('f_name', models.CharField(blank=True, max_length=30, null=True)),
                ('l_name', models.CharField(blank=True, max_length=30, null=True)),
                ('phone', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='financeapplication',
            name='frequency',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='financeapplication',
            name='other_info',
            field=models.TextField(blank=True, max_length=150, null=True),
        ),
    ]
