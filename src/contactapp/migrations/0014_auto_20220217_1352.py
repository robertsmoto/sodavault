# Generated by Django 3.2 on 2022-02-17 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contactapp', '0013_auto_20220217_1351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='companies',
        ),
        migrations.RemoveField(
            model_name='person',
            name='stores',
        ),
        migrations.RemoveField(
            model_name='person',
            name='suppliers',
        ),
        migrations.RemoveField(
            model_name='person',
            name='warehouses',
        ),
        migrations.RemoveField(
            model_name='person',
            name='websites',
        ),
    ]
