# Generated by Django 3.2 on 2022-02-13 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0072_alter_item_sku'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='sku',
            field=models.CharField(default='SKU-d3f2a9f6-be2e-427d-b25b', max_length=100, unique=True),
        ),
    ]
