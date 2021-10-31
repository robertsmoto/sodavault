# Generated by Django 3.2.3 on 2021-10-11 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='company_type',
            field=models.CharField(blank=True, choices=[('BLOG', 'Blog'), ('LOCA', 'Location'), ('SUPP', 'Suppplier'), ('CUST', 'Customer')], max_length=4),
        ),
    ]
