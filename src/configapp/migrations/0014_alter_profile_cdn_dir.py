# Generated by Django 3.2 on 2022-02-25 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configapp', '0013_auto_20220225_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cdn_dir',
            field=models.CharField(default='4cd0328a-19f5', help_text='User root cdn dir.eg. https://cdn.sodavault.com/image_dir/Y/m/d/image.webp', max_length=20),
        ),
    ]