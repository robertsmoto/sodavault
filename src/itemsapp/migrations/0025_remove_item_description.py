# Generated by Django 3.2.3 on 2021-12-24 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0024_auto_20211012_1406'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='description',
        ),
    ]