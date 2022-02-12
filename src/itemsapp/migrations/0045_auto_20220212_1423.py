# Generated by Django 3.2 on 2022-02-12 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0044_auto_20220212_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='cost',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='cost_shipping',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='sku',
            field=models.CharField(default='SKU-045aa37e-2abc-4dbd-9215', max_length=100, unique=True),
        ),
    ]
