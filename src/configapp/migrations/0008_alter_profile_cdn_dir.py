# Generated by Django 3.2 on 2022-02-25 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configapp', '0007_auto_20220225_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cdn_dir',
            field=models.CharField(default='36034761-e7c6', help_text='User root cdn dir.eg. https://cdn.sodavault.com/image_dir/Y/m/d/image.webp', max_length=20),
        ),
    ]
