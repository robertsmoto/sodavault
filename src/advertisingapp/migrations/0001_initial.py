# Generated by Django 3.2.3 on 2021-08-23 17:30

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('itemsapp', '0001_initial'),
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
                ('image_xl', imagekit.models.fields.ProcessedImageField(blank=True, help_text='auto rsizes to 1140px x 380px', null=True, upload_to='ad_banners/%Y/%m/%d')),
                ('image_lg', imagekit.models.fields.ProcessedImageField(blank=True, help_text='auto resizes to 960px x 320px', null=True, upload_to='ad_banners/%Y/%m/%d')),
                ('image_md', imagekit.models.fields.ProcessedImageField(blank=True, help_text='auto resizes to 720px x 240px', null=True, upload_to='ad_banners/%Y/%m/%d')),
                ('image_sm', imagekit.models.fields.ProcessedImageField(blank=True, help_text='auto resizes to 540px x 180px', null=True, upload_to='ad_banners/%Y/%m/%d')),
                ('image_skyscraper', imagekit.models.fields.ProcessedImageField(blank=True, help_text='160px x 600px', null=True, upload_to='ad_banners/%Y/%m/%d')),
                ('campaign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='banners', to='advertisingapp.campaign')),
            ],
            options={
                'verbose_name_plural': 'Banners',
            },
        ),
        migrations.CreateModel(
            name='Assett',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, verbose_name='Asset Name')),
                ('excerpt', ckeditor.fields.RichTextField(blank=True, help_text='400 characters max', max_length=400, null=True, verbose_name='Excerpt')),
                ('img_1x1', imagekit.models.fields.ProcessedImageField(blank=True, help_text='250px x 250px', null=True, upload_to='advertisingapp/assetts/%Y/%m/%d')),
                ('url_name', models.CharField(blank=True, help_text='URL tool tip on mouse hover.', max_length=70, verbose_name='URL Name')),
                ('url_link', models.URLField(blank=True, help_text="End url with '/'", max_length=100, verbose_name='URL')),
                ('campaign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assetts', to='advertisingapp.campaign')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assetts', to='itemsapp.product')),
            ],
            options={
                'verbose_name_plural': 'Ad Assetts',
            },
        ),
    ]
