# Generated by Django 3.2 on 2022-02-14 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0079_auto_20220214_1541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='parent',
        ),
        migrations.AddField(
            model_name='item',
            name='collection_quantity',
            field=models.IntegerField(default=1, help_text='How many items are included.'),
        ),
        migrations.AddField(
            model_name='item',
            name='component_parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='components', to='itemsapp.item'),
        ),
        migrations.AddField(
            model_name='item',
            name='component_quantity',
            field=models.IntegerField(default=1, help_text='How many components are included in the cost of 1 item.'),
        ),
        migrations.AddField(
            model_name='item',
            name='order_max',
            field=models.IntegerField(default=0, help_text='Use to limit order quantity.'),
        ),
        migrations.AddField(
            model_name='item',
            name='order_min',
            field=models.IntegerField(default=0, help_text='Use to require minium order quantity.'),
        ),
        migrations.AddField(
            model_name='item',
            name='product_parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='itemsapp.item'),
        ),
        migrations.AlterField(
            model_name='item',
            name='sku',
            field=models.CharField(default='SKU-eea7e54f-7a86-41a5-b5ab', max_length=100, unique=True),
        ),
    ]
