# Generated by Django 3.2 on 2022-03-02 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configapp', '0062_auto_20220302_0846'),
        ('contactapp', '0011_remove_company_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='stores',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='suppliers',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='warehouses',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='websites',
        ),
        migrations.AddField(
            model_name='company',
            name='categories',
            field=models.ManyToManyField(blank=True, to='configapp.Category'),
        ),
        migrations.AddField(
            model_name='company',
            name='tags',
            field=models.ManyToManyField(blank=True, to='configapp.Tag'),
        ),
    ]
