# Generated by Django 3.2 on 2022-03-04 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configapp', '0101_alter_profile_cdn_dir'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cdn_dir',
            field=models.CharField(default='243a88db-e1fb', help_text='User root cdn dir.eg. https://cdn.sodavault.com/image_dir/Y/m/d/image.webp', max_length=20),
        ),
    ]
