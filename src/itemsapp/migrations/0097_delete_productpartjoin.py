# Generated by Django 3.2 on 2022-02-15 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0096_alter_item_sku'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductPartJoin',
        ),
    ]
