# Generated by Django 3.2 on 2022-03-01 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configapp', '0049_alter_profile_cdn_dir'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cdn_dir',
            field=models.CharField(default='222c12aa-05bd', help_text='User root cdn dir.eg. https://cdn.sodavault.com/image_dir/Y/m/d/image.webp', max_length=20),
        ),
    ]