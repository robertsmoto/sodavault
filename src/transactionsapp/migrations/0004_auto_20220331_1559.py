# Generated by Django 3.2 on 2022-03-31 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactionsapp', '0003_auto_20220320_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asn',
            name='number',
            field=models.CharField(default='ASN-2022-03-31', max_length=100),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='number',
            field=models.CharField(default='ASN-2022-03-31', max_length=100),
        ),
    ]
