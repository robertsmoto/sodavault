# Generated by Django 3.2.3 on 2021-12-24 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisingapp', '0007_rename_img_1xl_assett_img_1x1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assett',
            name='img_1x1',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='image_skyscraper',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='image_xl',
        ),
    ]