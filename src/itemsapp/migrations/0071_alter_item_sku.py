# Generated by Django 3.2 on 2022-02-13 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0070_alter_item_sku'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='sku',
            field=models.CharField(default='SKU-2bdcdd2b-cdac-4f75-9fa7', max_length=100, unique=True),
        ),
    ]
