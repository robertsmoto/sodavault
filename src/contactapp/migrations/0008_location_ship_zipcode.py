# Generated by Django 3.2 on 2022-02-17 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactapp', '0007_auto_20220217_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='ship_zipcode',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
