# Generated by Django 3.2 on 2022-02-12 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0045_auto_20220212_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='cost',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bid',
            name='cost_quantity',
            field=models.IntegerField(default=1, help_text='Divides total cost by this number to return ecpu.'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='cost_shipping',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='sku',
            field=models.CharField(default='SKU-9ac7163c-79e9-40b8-872d', max_length=100, unique=True),
        ),
    ]
