# Generated by Django 3.2 on 2022-02-07 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0023_remove_item_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attributeitemjoin',
            old_name='attribute',
            new_name='attributes',
        ),
        migrations.RenameField(
            model_name='attributeitemjoin',
            old_name='term',
            new_name='terms',
        ),
        migrations.AddField(
            model_name='item',
            name='attributes',
            field=models.ManyToManyField(blank=True, to='itemsapp.AttributeItemJoin'),
        ),
        migrations.AddIndex(
            model_name='item',
            index=models.Index(fields=['sku'], name='itemsapp_it_sku_27a3ad_idx'),
        ),
    ]