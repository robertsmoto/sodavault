# Generated by Django 3.2 on 2022-03-02 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactapp', '0021_company_location_store_supplier_warehouse_website'),
        ('blogapp', '0021_auto_20220302_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='websites',
            field=models.ManyToManyField(blank=True, to='contactapp.Website'),
        ),
    ]
