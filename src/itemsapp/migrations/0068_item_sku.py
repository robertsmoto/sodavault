# Generated by Django 3.2 on 2022-02-13 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0067_auto_20220213_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='sku',
            field=models.CharField(default='SKU-3ab2ad70-b3ea-4fb8-b112', max_length=100, unique=True),
        ),
    ]
