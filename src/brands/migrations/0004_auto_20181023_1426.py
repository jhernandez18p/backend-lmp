# Generated by Django 2.1 on 2018-10-23 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brands', '0003_auto_20180824_0835'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brand',
            options={'ordering': ['name'], 'verbose_name': 'Marca', 'verbose_name_plural': 'Marcas'},
        ),
        migrations.AddField(
            model_name='brand',
            name='count',
            field=models.CharField(blank=True, max_length=140),
        ),
    ]
