# Generated by Django 3.2 on 2022-02-13 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledgerapp', '0008_auto_20220213_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='identification',
            field=models.CharField(default='BATCH-3f8a9a2c-b45c-4609-b7f6', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='lot',
            name='identification',
            field=models.CharField(default='LOT-0515faf1-e4e8-41bb-9c15', max_length=100, unique=True),
        ),
    ]
