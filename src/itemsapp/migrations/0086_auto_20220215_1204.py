# Generated by Django 3.2 on 2022-02-15 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0085_auto_20220215_0953'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComponentJoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, help_text='How many components are included in the cost of 1 item.')),
            ],
        ),
        migrations.RemoveField(
            model_name='item',
            name='component_quantity',
        ),
        migrations.RemoveField(
            model_name='item',
            name='components',
        ),
        migrations.RemoveField(
            model_name='item',
            name='cost',
        ),
        migrations.RemoveField(
            model_name='item',
            name='cost_quantity',
        ),
        migrations.RemoveField(
            model_name='item',
            name='cost_shipping',
        ),
        migrations.AlterField(
            model_name='item',
            name='sku',
            field=models.CharField(default='SKU-4bdb4c2e-6405-480a-8390', max_length=100, unique=True),
        ),
    ]