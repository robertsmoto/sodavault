# Generated by Django 3.2 on 2022-02-21 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0118_remove_attributejoin_terms'),
    ]

    operations = [
        migrations.AddField(
            model_name='attributejoin',
            name='terms',
            field=models.ManyToManyField(blank=True, to='itemsapp.ItemAttribute'),
        ),
    ]
