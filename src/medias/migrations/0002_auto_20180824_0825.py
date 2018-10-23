# Generated by Django 2.1 on 2018-08-24 13:25

from django.db import migrations, models
import src.medias.models


class Migration(migrations.Migration):

    dependencies = [
        ('medias', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='hight',
            field=models.ImageField(blank=True, default='/photos/lmp.jpg', upload_to=src.medias.models.get_upload_path),
        ),
        migrations.AlterField(
            model_name='photo',
            name='low',
            field=models.ImageField(blank=True, default='/photos/lmp.jpg', upload_to=src.medias.models.get_upload_path),
        ),
        migrations.AlterField(
            model_name='photo',
            name='thumb',
            field=models.ImageField(blank=True, default='/photos/lmp.jpg', upload_to=src.medias.models.get_upload_path),
        ),
    ]
