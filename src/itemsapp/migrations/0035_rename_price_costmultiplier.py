# Generated by Django 3.2 on 2022-02-11 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0034_auto_20220211_0828'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Price',
            new_name='CostMultiplier',
        ),
    ]