# Generated by Django 3.2 on 2022-02-06 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0010_attribute'),
    ]

    operations = [
        migrations.AddField(
            model_name='term',
            name='attribute',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.attribute'),
        ),
    ]