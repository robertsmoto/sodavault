# Generated by Django 3.2 on 2022-02-24 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configapp', '0037_auto_20220224_0928'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='image_any',
            new_name='img_any',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='caption',
            new_name='img_caption',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='lg_11',
            new_name='img_lg_11',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='lg_191',
            new_name='img_lg_191',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='lg_21',
            new_name='img_lg_21',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='md_11',
            new_name='img_md_11',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='md_21',
            new_name='img_md_21',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='sm_11',
            new_name='img_sm_11',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='sm_21',
            new_name='img_sm_21',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='title',
            new_name='img_title',
        ),
        migrations.AlterField(
            model_name='profile',
            name='cdn_dir',
            field=models.CharField(default='01648c46-05f2', help_text='User root cdn dir.eg. https://cdn.sodavault.com/image_dir/Y/m/d/image.webp', max_length=20),
        ),
    ]
