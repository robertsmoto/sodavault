# Generated by Django 3.2 on 2022-02-13 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactapp', '0005_auto_20220213_1004'),
        ('blogapp', '0010_alter_post_locations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='locations',
        ),
        migrations.AddField(
            model_name='post',
            name='websites',
            field=models.ManyToManyField(blank=True, to='contactapp.Website'),
        ),
    ]
