# Generated by Django 3.2 on 2022-02-11 00:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0032_auto_20220210_2339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='calculated_price',
        ),
        migrations.RemoveField(
            model_name='item',
            name='calculated_stock_quantity',
        ),
        migrations.RemoveField(
            model_name='item',
            name='ecpu',
        ),
        migrations.RemoveField(
            model_name='item',
            name='ecpu_calc_from',
        ),
        migrations.RemoveField(
            model_name='item',
            name='ecpu_override',
        ),
        migrations.RemoveField(
            model_name='item',
            name='price_calc_from',
        ),
        migrations.RemoveField(
            model_name='item',
            name='price_override',
        ),
        migrations.RemoveField(
            model_name='item',
            name='stock_quantity',
        ),
        migrations.RemoveField(
            model_name='item',
            name='unit_override',
        ),
        migrations.RemoveField(
            model_name='item',
            name='use_calculated_price',
        ),
        migrations.RemoveField(
            model_name='item',
            name='use_calculated_quantity',
        ),
        migrations.RemoveField(
            model_name='item',
            name='use_subitem_sum',
        ),
    ]
