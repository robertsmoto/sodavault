# Generated by Django 3.2 on 2022-02-06 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0005_attribute'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='new_field_two',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]