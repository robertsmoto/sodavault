# Generated by Django 3.2.3 on 2021-12-25 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisingapp', '0012_auto_20211225_0643'),
    ]

    operations = [
        migrations.RenameField(
            model_name='banner',
            old_name='ban_med_square',
            new_name='ban_md_square',
        ),
    ]
