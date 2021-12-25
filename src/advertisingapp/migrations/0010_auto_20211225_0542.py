# Generated by Django 3.2.3 on 2021-12-25 05:42

import advertisingapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisingapp', '0009_auto_20211224_2048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assett',
            name='img_1x1',
        ),
        migrations.AddField(
            model_name='assett',
            name='image',
            field=models.ImageField(blank=True, help_text='recommended size: 1000px x 1000px', null=True, upload_to=advertisingapp.models.new_filename_assett),
        ),
        migrations.AlterField(
            model_name='banner',
            name='image_skyscraper',
            field=models.ImageField(blank=True, help_text='recommended size: 160px x 600px', null=True, upload_to=advertisingapp.models.new_filename_banner),
        ),
        migrations.AlterField(
            model_name='banner',
            name='image_xl',
            field=models.ImageField(blank=True, help_text='recommended size: 1140px x 380px', null=True, upload_to=advertisingapp.models.new_filename_banner),
        ),
    ]
