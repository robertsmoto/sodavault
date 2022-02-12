# Generated by Django 3.2 on 2022-02-12 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0043_auto_20220212_1206'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='quantity',
            new_name='cost_quantity',
        ),
        migrations.RenameField(
            model_name='bid',
            old_name='shipping',
            new_name='cost_shipping',
        ),
        migrations.AddField(
            model_name='item',
            name='cost_quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='item',
            name='sku',
            field=models.CharField(default='SKU-539ef8e8-2f9f-42c7-9605', max_length=100, unique=True),
        ),
    ]
