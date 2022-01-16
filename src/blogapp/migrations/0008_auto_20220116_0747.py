# Generated by Django 3.2 on 2022-01-16 07:47

from django.db import migrations, models
import utilities.utils_images


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0007_alter_post_menu_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image_191',
            field=models.ImageField(blank=True, help_text='1.9:1 ratio recommended size 1200px x 630px', null=True, upload_to=utilities.utils_images.new_filename_blog_cat),
        ),
        migrations.AddField(
            model_name='category',
            name='image_21',
            field=models.ImageField(blank=True, help_text='recommended size 1200px x 600px', null=True, upload_to=utilities.utils_images.new_filename_blog_cat),
        ),
        migrations.AddField(
            model_name='category',
            name='keywords',
            field=models.CharField(blank=True, help_text='Comma-separated values.', max_length=100, verbose_name='Category Keywords'),
        ),
        migrations.AddField(
            model_name='tag',
            name='description',
            field=models.CharField(blank=True, max_length=100, verbose_name='Tag Description'),
        ),
        migrations.AddField(
            model_name='tag',
            name='image',
            field=models.ImageField(blank=True, help_text='recommended size 500px x 500px', null=True, upload_to=utilities.utils_images.new_filename_blog_tag),
        ),
        migrations.AddField(
            model_name='tag',
            name='image_191',
            field=models.ImageField(blank=True, help_text='1.9:1 ratio recommended size 1200px x 630px', null=True, upload_to=utilities.utils_images.new_filename_blog_tag),
        ),
        migrations.AddField(
            model_name='tag',
            name='image_21',
            field=models.ImageField(blank=True, help_text='recommended size 1200px x 600px', null=True, upload_to=utilities.utils_images.new_filename_blog_tag),
        ),
        migrations.AddField(
            model_name='tag',
            name='image_lg_square',
            field=models.CharField(blank=True, help_text='automatic size: 500px x 500px', max_length=200),
        ),
        migrations.AddField(
            model_name='tag',
            name='image_md_square',
            field=models.CharField(blank=True, help_text='automatic size: 250px x 250px', max_length=200),
        ),
        migrations.AddField(
            model_name='tag',
            name='image_sm_square',
            field=models.CharField(blank=True, help_text='automatic size: 200px x 200px', max_length=200),
        ),
        migrations.AddField(
            model_name='tag',
            name='keywords',
            field=models.CharField(blank=True, help_text='Comma-separated values.', max_length=100, verbose_name='Tag Keywords'),
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, help_text='recommended size 500px x 500px', null=True, upload_to=utilities.utils_images.new_filename_blog_cat),
        ),
    ]