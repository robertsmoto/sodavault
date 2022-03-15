# Generated by Django 3.2 on 2022-03-04 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0042_ledger'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemassemblyjoin',
            name='is_unlimited',
            field=models.BooleanField(default=False, help_text='Is not limited by inventory eg. skilled labor.'),
        ),
        migrations.AddField(
            model_name='itemassemblyjoin',
            name='use_all',
            field=models.BooleanField(default=False, help_text='Use the entire quantity when creating a parent item. eg. labels'),
        ),
    ]
