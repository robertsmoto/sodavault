# Generated by Django 3.2 on 2022-03-03 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactionsapp', '0013_auto_20220302_1249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asndetails',
            name='item',
        ),
        migrations.AlterField(
            model_name='asn',
            name='number',
            field=models.CharField(default='ASN-2022-03-03', max_length=100),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='number',
            field=models.CharField(default='ASN-2022-03-03', max_length=100),
        ),
    ]
