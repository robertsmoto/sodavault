# Generated by Django 3.2.3 on 2021-10-11 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0007_auto_20211011_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='items', to='itemsapp.Category'),
        ),
        migrations.AddField(
            model_name='item',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='items', to='itemsapp.Tag'),
        ),
    ]
