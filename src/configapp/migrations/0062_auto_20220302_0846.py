# Generated by Django 3.2 on 2022-03-02 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configapp', '0061_alter_profile_cdn_dir'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='store',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='warehouse',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='warehouse',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='website',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='website',
            name='tags',
        ),
        migrations.AlterField(
            model_name='profile',
            name='cdn_dir',
            field=models.CharField(default='16b7d13d-eec9', help_text='User root cdn dir.eg. https://cdn.sodavault.com/image_dir/Y/m/d/image.webp', max_length=20),
        ),
    ]
