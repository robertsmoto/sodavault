# Generated by Django 3.2.3 on 2021-12-24 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisingapp', '0006_auto_20211224_1923'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assett',
            old_name='img_1xl',
            new_name='img_1x1',
        ),
    ]