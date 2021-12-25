# Generated by Django 3.2.3 on 2021-12-25 06:28

import advertisingapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisingapp', '0010_auto_20211225_0542'),
    ]

    operations = [
        migrations.RenameField(
            model_name='banner',
            old_name='image_skyscraper',
            new_name='ban_skyscraper',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='image_lg',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='image_md',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='image_sm',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='image_xl',
        ),
        migrations.AddField(
            model_name='banner',
            name='ban_inline_rectangle',
            field=models.ImageField(blank=True, help_text='recommended size: 300px x 250px', null=True, upload_to=advertisingapp.models.new_filename_banner),
        ),
        migrations.AddField(
            model_name='banner',
            name='ban_leaderboard',
            field=models.ImageField(blank=True, help_text='recommended size: 728px x 90px', null=True, upload_to=advertisingapp.models.new_filename_banner),
        ),
        migrations.AddField(
            model_name='banner',
            name='ban_lg_leaderboard',
            field=models.ImageField(blank=True, help_text='recommended size: 970px x 90px', null=True, upload_to=advertisingapp.models.new_filename_banner),
        ),
        migrations.AddField(
            model_name='banner',
            name='ban_lg_rectangle',
            field=models.ImageField(blank=True, help_text='recommended size: 336px x 280px', null=True, upload_to=advertisingapp.models.new_filename_banner),
        ),
        migrations.AddField(
            model_name='banner',
            name='ban_lg_square',
            field=models.CharField(blank=True, help_text='automatic size: 500px x 500px', max_length=200),
        ),
        migrations.AddField(
            model_name='banner',
            name='ban_med_square',
            field=models.CharField(blank=True, help_text='automatic size: 250px x 250px', max_length=200),
        ),
        migrations.AddField(
            model_name='banner',
            name='ban_sm_square',
            field=models.CharField(blank=True, help_text='automatic size: 200px x 200px', max_length=200),
        ),
        migrations.AddField(
            model_name='banner',
            name='ban_square',
            field=models.ImageField(blank=True, help_text='recommended size: 500px x 500px', null=True, upload_to=advertisingapp.models.new_filename_banner),
        ),
    ]