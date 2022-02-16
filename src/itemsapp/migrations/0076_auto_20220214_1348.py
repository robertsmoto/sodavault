# Generated by Django 3.2 on 2022-02-14 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0075_auto_20220214_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='components',
            field=models.ManyToManyField(blank=True, related_name='_itemsapp_item_components_+', to='itemsapp.Item'),
        ),
        migrations.AlterField(
            model_name='item',
            name='sku',
            field=models.CharField(default='SKU-bb649ac9-a36e-42d7-abbf', max_length=100, unique=True),
        ),
    ]
