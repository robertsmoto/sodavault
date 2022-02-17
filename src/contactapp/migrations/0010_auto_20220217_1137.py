# Generated by Django 3.2 on 2022-02-17 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contactapp', '0009_rename_shop_zipcode_person_ship_zipcode'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ['lastname', 'firstname'], 'verbose_name': 'c. Contact', 'verbose_name_plural': 'c. Contacts'},
        ),
        migrations.RemoveField(
            model_name='person',
            name='location',
        ),
        migrations.AddField(
            model_name='person',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contactapp.location'),
        ),
    ]
