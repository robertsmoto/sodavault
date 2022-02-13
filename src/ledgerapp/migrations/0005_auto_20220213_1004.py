# Generated by Django 3.2 on 2022-02-13 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contactapp', '0004_auto_20220213_1004'),
        ('ledgerapp', '0004_auto_20220213_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='Entry',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contactapp.location'),
        ),
        migrations.AlterField(
            model_name='batch',
            name='identification',
            field=models.CharField(default='BATCH-a1973542-62f4-4d04-9494', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='lot',
            name='identification',
            field=models.CharField(default='LOT-81ee3e8e-addd-4bb2-8d3b', max_length=100, unique=True),
        ),
    ]
