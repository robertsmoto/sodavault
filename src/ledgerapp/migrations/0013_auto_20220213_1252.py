# Generated by Django 3.2 on 2022-02-13 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledgerapp', '0012_auto_20220213_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='batch',
            name='identification',
        ),
        migrations.RemoveField(
            model_name='lot',
            name='identification',
        ),
    ]