# Generated by Django 3.2 on 2022-02-13 05:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configapp', '0011_currency_currencyconfig'),
        ('ledgerapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='parts',
            new_name='part',
        ),
        migrations.RenameField(
            model_name='entry',
            old_name='products',
            new_name='product',
        ),
        migrations.RemoveField(
            model_name='batch',
            name='number',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='batches',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='locations',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='lots',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='number',
        ),
        migrations.AddField(
            model_name='batch',
            name='identification',
            field=models.CharField(default='BATCH-ffbe3f5b-b8c0-4408-9122', max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='batch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ledgerapp.batch'),
        ),
        migrations.AddField(
            model_name='entry',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='configapp.location'),
        ),
        migrations.AddField(
            model_name='entry',
            name='lot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ledgerapp.lot'),
        ),
        migrations.AddField(
            model_name='lot',
            name='identification',
            field=models.CharField(default='LOT-2d018c67-9d05-4b14-b2c0', max_length=100, unique=True),
        ),
    ]
