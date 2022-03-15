# Generated by Django 3.2 on 2022-02-25 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactionsapp', '0002_auto_20220225_1324'),
        ('ledgerapp', '0002_auto_20220225_1324'),
        ('itemsapp', '0002_remove_bid_supplier'),
        ('contactapp', '0003_auto_20220225_1127'),
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
        migrations.DeleteModel(
            name='Company',
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Store',
        ),
        migrations.DeleteModel(
            name='Supplier',
        ),
        migrations.DeleteModel(
            name='Warehouse',
        ),
        migrations.DeleteModel(
            name='Website',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]
