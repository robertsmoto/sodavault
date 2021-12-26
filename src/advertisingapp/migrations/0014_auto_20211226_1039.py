# Generated by Django 3.2.3 on 2021-12-26 10:39

from django.db import migrations, models
import utilities.utils_images


class Migration(migrations.Migration):

    dependencies = [
        ('advertisingapp', '0013_rename_ban_med_square_banner_ban_md_square'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='ban_inline_rectangle',
            field=models.ImageField(blank=True, help_text='recommended size: 300px x 250px', null=True, upload_to=utilities.utils_images.new_filename_banner),
        ),
        migrations.AlterField(
            model_name='banner',
            name='ban_leaderboard',
            field=models.ImageField(blank=True, help_text='recommended size: 728px x 90px', null=True, upload_to=utilities.utils_images.new_filename_banner),
        ),
        migrations.AlterField(
            model_name='banner',
            name='ban_lg_leaderboard',
            field=models.ImageField(blank=True, help_text='recommended size: 970px x 90px', null=True, upload_to=utilities.utils_images.new_filename_banner),
        ),
        migrations.AlterField(
            model_name='banner',
            name='ban_lg_rectangle',
            field=models.ImageField(blank=True, help_text='recommended size: 336px x 280px', null=True, upload_to=utilities.utils_images.new_filename_banner),
        ),
        migrations.AlterField(
            model_name='banner',
            name='ban_skyscraper',
            field=models.ImageField(blank=True, help_text='recommended size: 160px x 600px', null=True, upload_to=utilities.utils_images.new_filename_banner),
        ),
        migrations.AlterField(
            model_name='banner',
            name='ban_square',
            field=models.ImageField(blank=True, help_text='recommended size: 500px x 500px', null=True, upload_to=utilities.utils_images.new_filename_banner),
        ),
    ]