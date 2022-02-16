# Generated by Django 3.2 on 2022-02-15 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0084_auto_20220215_0920'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='component_parent',
        ),
        migrations.AddField(
            model_name='item',
            name='components',
            field=models.ManyToManyField(blank=True, related_name='_itemsapp_item_components_+', to='itemsapp.Item'),
        ),
        migrations.AlterField(
            model_name='item',
            name='sku',
            field=models.CharField(default='SKU-030ed4b2-c9c6-41df-a883', max_length=100, unique=True),
        ),
    ]
