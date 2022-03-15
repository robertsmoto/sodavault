# Generated by Django 3.2 on 2022-03-02 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0018_auto_20220302_0940'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doc',
            name='author',
        ),
        migrations.RemoveField(
            model_name='doc',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='doc',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='doc',
            name='post_ptr',
        ),
        migrations.RemoveField(
            model_name='doc',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='page',
            name='author',
        ),
        migrations.RemoveField(
            model_name='page',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='page',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='page',
            name='post_ptr',
        ),
        migrations.RemoveField(
            model_name='page',
            name='tags',
        ),
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.DeleteModel(
            name='Doc',
        ),
        migrations.DeleteModel(
            name='Page',
        ),
    ]
