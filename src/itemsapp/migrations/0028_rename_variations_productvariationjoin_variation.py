# Generated by Django 3.2 on 2022-03-01 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0027_auto_20220301_1344'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productvariationjoin',
            old_name='variations',
            new_name='variation',
        ),
    ]