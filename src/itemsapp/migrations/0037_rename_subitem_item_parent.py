# Generated by Django 3.2 on 2022-02-11 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0036_item_cost_multiplier'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='subitem',
            new_name='parent',
        ),
    ]