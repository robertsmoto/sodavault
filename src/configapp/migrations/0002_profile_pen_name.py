# Generated by Django 3.2 on 2021-12-28 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='pen_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]