# Generated by Django 3.2 on 2022-02-06 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledgerapp', '0001_initial'),
        ('transactionsapp', '0002_remove_bid_digital_products'),
        ('itemsapp', '0016_auto_20220206_1322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productpartjoin',
            name='digital_products',
        ),
        migrations.DeleteModel(
            name='DigitalProduct',
        ),
    ]