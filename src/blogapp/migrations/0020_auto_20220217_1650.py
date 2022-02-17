# Generated by Django 3.2 on 2022-02-17 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0019_postcategory_posttag'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='post_categories', to='blogapp.PostCategory'),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='post_tags', to='blogapp.PostTag'),
        ),
    ]
