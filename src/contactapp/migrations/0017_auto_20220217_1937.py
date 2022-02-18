# Generated by Django 3.2 on 2022-02-17 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contactapp', '0016_auto_20220217_1921'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['name'], 'verbose_name': 'Company', 'verbose_name_plural': 'Companies'},
        ),
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ['lastname', 'firstname'], 'verbose_name': 'Contact', 'verbose_name_plural': 'Contacts'},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['lastname', 'firstname'], 'verbose_name': 'Customer', 'verbose_name_plural': 'Customers'},
        ),
        migrations.AlterModelOptions(
            name='store',
            options={'ordering': ['name'], 'verbose_name': 'Store', 'verbose_name_plural': 'Stores'},
        ),
        migrations.AlterModelOptions(
            name='supplier',
            options={'ordering': ['name'], 'verbose_name': 'Supplier', 'verbose_name_plural': 'Suppliers'},
        ),
        migrations.AlterModelOptions(
            name='warehouse',
            options={'ordering': ['name'], 'verbose_name': 'Warehouse', 'verbose_name_plural': 'Warehouses'},
        ),
        migrations.AlterModelOptions(
            name='website',
            options={'ordering': ['name'], 'verbose_name': 'Website', 'verbose_name_plural': 'Websites'},
        ),
    ]
