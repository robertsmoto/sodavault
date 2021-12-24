# Generated by Django 3.2.3 on 2021-12-24 19:23

import advertisingapp.models
from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('advertisingapp', '0005_auto_20211222_0713'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assett',
            name='img_1x1',
        ),
        migrations.AddField(
            model_name='assett',
            name='img_1xl',
            field=imagekit.models.fields.ProcessedImageField(blank=True, help_text='recommended size: 250px x 250px', null=True, upload_to=advertisingapp.models.new_filename_assett),
        ),
        migrations.AlterField(
            model_name='banner',
            name='image_skyscraper',
            field=imagekit.models.fields.ProcessedImageField(blank=True, help_text='recommended size: 160px x 600px', null=True, upload_to=advertisingapp.models.new_filename_banner),
        ),
        migrations.AlterField(
            model_name='banner',
            name='image_xl',
            field=imagekit.models.fields.ProcessedImageField(blank=True, help_text='recommended size: 1140px x 380px', null=True, upload_to=advertisingapp.models.new_filename_banner),
        ),
    ]
