# Generated by Django 3.2 on 2022-02-13 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0061_alter_item_sku'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='sku',
            field=models.CharField(default='SKU-999eceda-a686-468b-818c', max_length=100, unique=True),
        ),
    ]