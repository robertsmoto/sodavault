# Generated by Django 3.2 on 2022-02-25 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configapp', '0009_auto_20220225_1346'),
        ('contactapp', '0005_company_contact_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='stores',
            field=models.ManyToManyField(blank=True, to='configapp.Store'),
        ),
        migrations.AddField(
            model_name='contact',
            name='warehouses',
            field=models.ManyToManyField(blank=True, to='configapp.Warehouse'),
        ),
        migrations.AddField(
            model_name='contact',
            name='websites',
            field=models.ManyToManyField(blank=True, to='configapp.Website'),
        ),
    ]