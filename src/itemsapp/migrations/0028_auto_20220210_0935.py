# Generated by Django 3.2 on 2022-02-10 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0027_attribute_category_department_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='categories', to='itemsapp.Category'),
        ),
        migrations.AddField(
            model_name='item',
            name='departments',
            field=models.ManyToManyField(blank=True, related_name='departments', to='itemsapp.Department'),
        ),
        migrations.AddField(
            model_name='item',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tags', to='itemsapp.Tag'),
        ),
    ]