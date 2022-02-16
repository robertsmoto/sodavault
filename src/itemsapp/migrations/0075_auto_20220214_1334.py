# Generated by Django 3.2 on 2022-02-14 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0074_alter_item_sku'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='parent',
        ),
        migrations.AlterField(
            model_name='item',
            name='sku',
            field=models.CharField(default='SKU-6a1c25e1-d57e-486d-a43d', max_length=100, unique=True),
        ),
    ]