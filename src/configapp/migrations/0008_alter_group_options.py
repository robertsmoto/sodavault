# Generated by Django 3.2 on 2022-02-10 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configapp', '0007_auto_20220210_1116'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['order', 'name'], 'verbose_name_plural': '05. Groups'},
        ),
    ]
