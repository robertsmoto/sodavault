# Generated by Django 3.2.3 on 2021-12-22 07:13

import advertisingapp.models
from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('advertisingapp', '0004_auto_20211220_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='image_lg',
            field=models.CharField(blank=True, default=1987, help_text='automatic size: 960px x 320px', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='banner',
            name='image_md',
            field=models.CharField(blank=True, default=1987, help_text='automatic size: 720px x 240px', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='banner',
            name='image_skyscraper',
            field=imagekit.models.fields.ProcessedImageField(blank=True, help_text='recommended size: 160px x 600px', null=True, upload_to=""),
        ),
        migrations.AlterField(
            model_name='banner',
            name='image_sm',
            field=models.CharField(blank=True, default=1987, help_text='automatic size: 540px x 180px', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='banner',
            name='image_xl',
            field=imagekit.models.fields.ProcessedImageField(blank=True, help_text='recommended size: 1140px x 380px', null=True, upload_to=""),
        ),
    ]
