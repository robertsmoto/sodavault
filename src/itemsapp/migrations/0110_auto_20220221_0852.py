# Generated by Django 3.2 on 2022-02-21 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0109_item_attributes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attributejoin',
            name='display_order',
        ),
        migrations.AddField(
            model_name='attributejoin',
            name='order',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
