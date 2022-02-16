# Generated by Django 3.2 on 2022-02-15 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0082_auto_20220215_0902'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='components',
        ),
        migrations.AddField(
            model_name='item',
            name='component_parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='components', to='itemsapp.item'),
        ),
        migrations.AlterField(
            model_name='item',
            name='sku',
            field=models.CharField(default='SKU-09c41eb1-4e6a-4d75-801a', max_length=100, unique=True),
        ),
    ]
