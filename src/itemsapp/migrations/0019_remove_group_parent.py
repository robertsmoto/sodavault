# Generated by Django 3.2.3 on 2021-10-11 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0018_auto_20211011_1544'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='parent',
        ),
    ]
