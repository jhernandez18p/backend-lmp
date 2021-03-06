# Generated by Django 2.1 on 2018-08-24 12:13

from django.db import migrations, models
import src.brands.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=140)),
                ('slug', models.CharField(blank=True, max_length=140)),
                ('alt', models.CharField(blank=True, max_length=140)),
                ('img', models.ImageField(blank=True, default='/brands/lmp.jpg', null=True, upload_to=src.brands.models.get_upload_path)),
            ],
            options={
                'verbose_name': 'Marca',
                'verbose_name_plural': 'Marcas',
            },
        ),
    ]
