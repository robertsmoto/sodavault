# Generated by Django 3.2 on 2022-02-27 09:04

import configapp.utils.utils_images
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('configapp', '0036_alter_profile_cdn_dir'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cdn_dir',
            field=models.CharField(default='5303c383-e40b', help_text='User root cdn dir.eg. https://cdn.sodavault.com/image_dir/Y/m/d/image.webp', max_length=20),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lg_21', models.ImageField(blank=True, help_text='Recommended size: 2100px x 600px. Recommended name: name-21.jpg', null=True, storage=configapp.utils.utils_images.OverwriteStorage(), upload_to=configapp.utils.utils_images.new_filename)),
                ('lg_11', models.ImageField(blank=True, help_text='Recommended size: 500px x 500px Recommended name: name-11.jpg', null=True, storage=configapp.utils.utils_images.OverwriteStorage(), upload_to=configapp.utils.utils_images.new_filename)),
                ('custom', models.ImageField(blank=True, help_text='Image with custom size.', null=True, storage=configapp.utils.utils_images.OverwriteStorage(), upload_to=configapp.utils.utils_images.new_filename)),
                ('lg_191', models.ImageField(blank=True, help_text='1.9:1 ratio recommended size 2100px x 630px Recommended name: name-191.jpg', null=True, storage=configapp.utils.utils_images.OverwriteStorage(), upload_to=configapp.utils.utils_images.new_filename)),
                ('title', models.CharField(blank=True, help_text='Alt text for image.', max_length=200)),
                ('caption', models.CharField(blank=True, help_text='Caption for image.', max_length=200)),
                ('md_21', models.CharField(blank=True, help_text='Automatic size: 800px x 400px', max_length=200)),
                ('sm_21', models.CharField(blank=True, help_text='Automatic size: 400px x 200px', max_length=200)),
                ('md_11', models.CharField(blank=True, help_text='Automatic size: 250px x 250px', max_length=200)),
                ('sm_11', models.CharField(blank=True, help_text='Automatic size: 200px x 200px', max_length=200)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]