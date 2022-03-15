# Generated by Django 3.2 on 2022-03-03 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configapp', '0091_alter_profile_cdn_dir'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cdn_dir',
            field=models.CharField(default='2fe5ad0e-3386', help_text='User root cdn dir.eg. https://cdn.sodavault.com/image_dir/Y/m/d/image.webp', max_length=20),
        ),
    ]