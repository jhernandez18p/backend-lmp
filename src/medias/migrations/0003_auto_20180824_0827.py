# Generated by Django 2.1 on 2018-08-24 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medias', '0002_auto_20180824_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='position',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
