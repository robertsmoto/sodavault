# Generated by Django 3.2 on 2022-03-15 14:42

import ckeditor.fields
import configapp.utils.images
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Name of the Campaign', max_length=200)),
                ('site_name', models.CharField(blank=True, help_text='Text of site advertised, will show in the URL', max_length=200, verbose_name='Site Name')),
                ('site_url', models.URLField(blank=True, verbose_name='URL of advertised site')),
                ('url_analyticscode', models.CharField(blank=True, help_text='?utm_source=swimexpress&utm_medium=webads&utm_campaign=campaign_name', max_length=100, verbose_name='URL Analytics Code')),
                ('date_added', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Date Added')),
                ('date_expires', models.DateTimeField(blank=True, help_text='Leave blank = never expires', null=True, verbose_name='Expiration Date')),
                ('notes', ckeditor.fields.RichTextField(blank=True, help_text='Notes about how the campaign is used.', null=True, verbose_name='Notes')),
            ],
            options={
                'verbose_name_plural': 'Ad Campaigns',
            },
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Name of the Banner', max_length=200, verbose_name='Name')),
                ('excerpt', ckeditor.fields.RichTextField(blank=True, help_text='400 characters max', max_length=400, null=True, verbose_name='Excerpt')),
                ('url_name', models.CharField(blank=True, help_text='URL tool tip on mouse hover.', max_length=70, verbose_name='URL Name')),
                ('url_link', models.URLField(blank=True, help_text="End url with '/'", max_length=100, verbose_name='URL')),
                ('ban_square', models.ImageField(blank=True, help_text='recommended size: 500px x 500px', null=True, upload_to=configapp.utils.images.new_filename)),
                ('ban_leaderboard', models.ImageField(blank=True, help_text='recommended size: 728px x 90px', null=True, upload_to=configapp.utils.images.new_filename)),
                ('ban_lg_leaderboard', models.ImageField(blank=True, help_text='recommended size: 970px x 90px', null=True, upload_to=configapp.utils.images.new_filename)),
                ('ban_inline_rectangle', models.ImageField(blank=True, help_text='recommended size: 300px x 250px', null=True, upload_to=configapp.utils.images.new_filename)),
                ('ban_lg_rectangle', models.ImageField(blank=True, help_text='recommended size: 336px x 280px', null=True, upload_to=configapp.utils.images.new_filename)),
                ('ban_skyscraper', models.ImageField(blank=True, help_text='recommended size: 160px x 600px', null=True, upload_to=configapp.utils.images.new_filename)),
                ('ban_lg_square', models.CharField(blank=True, help_text='automatic size: 500px x 500px', max_length=200)),
                ('ban_md_square', models.CharField(blank=True, help_text='automatic size: 250px x 250px', max_length=200)),
                ('ban_sm_square', models.CharField(blank=True, help_text='automatic size: 200px x 200px', max_length=200)),
                ('campaign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='banners', to='advertisingapp.campaign')),
            ],
            options={
                'verbose_name_plural': 'Banners',
            },
        ),
    ]
