# Generated by Django 3.2 on 2022-02-13 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactapp', '0003_company_domain'),
        ('blogapp', '0008_auto_20220210_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='locations',
            field=models.ManyToManyField(blank=True, to='contactapp.Location'),
        ),
    ]
