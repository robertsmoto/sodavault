# Generated by Django 3.2 on 2022-03-01 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0018_auto_20220227_0947'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attribute',
            options={'ordering': ['slug'], 'verbose_name_plural': '_ attributes'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['slug'], 'verbose_name_plural': '_ categories'},
        ),
        migrations.AlterModelOptions(
            name='component',
            options={'ordering': ['sku']},
        ),
        migrations.AlterModelOptions(
            name='department',
            options={'ordering': ['slug'], 'verbose_name_plural': '_ departments'},
        ),
        migrations.AlterModelOptions(
            name='part',
            options={'ordering': ['sku']},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['sku']},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['slug'], 'verbose_name_plural': '_ tags'},
        ),
        migrations.AddField(
            model_name='image',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='image',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]