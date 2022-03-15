# Generated by Django 3.2 on 2022-02-27 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0013_delete_image'),
        ('configapp', '0034_auto_20220227_0858'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.AlterField(
            model_name='profile',
            name='cdn_dir',
            field=models.CharField(default='3425b308-071d', help_text='User root cdn dir.eg. https://cdn.sodavault.com/image_dir/Y/m/d/image.webp', max_length=20),
        ),
    ]