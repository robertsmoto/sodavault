# Generated by Django 3.2 on 2022-02-10 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configapp', '0005_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('domain', models.CharField(blank=True, max_length=200, verbose_name='Domain eg. example.com')),
                ('name', models.CharField(blank=True, max_length=200, verbose_name='Location Name')),
                ('description', models.CharField(blank=True, max_length=200, verbose_name='Location Description')),
            ],
            options={
                'verbose_name_plural': '01. Locations',
            },
        ),
    ]
