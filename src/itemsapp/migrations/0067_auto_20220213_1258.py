# Generated by Django 3.2 on 2022-02-13 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0066_alter_item_sku'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='item',
            name='itemsapp_it_sku_27a3ad_idx',
        ),
        migrations.RemoveField(
            model_name='item',
            name='sku',
        ),
    ]
