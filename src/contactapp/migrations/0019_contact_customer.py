# Generated by Django 3.2 on 2022-03-02 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contactapp', '0018_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('contactapp.person',),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('contactapp.person',),
        ),
    ]