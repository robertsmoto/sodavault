# Generated by Django 3.2 on 2022-02-11 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configapp', '0010_unit'),
        ('itemsapp', '0037_rename_subitem_item_parent'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitDisplay',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('configapp.unit',),
        ),
        migrations.CreateModel(
            name='UnitInventory',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('configapp.unit',),
        ),
        migrations.RemoveField(
            model_name='item',
            name='unit',
        ),
        migrations.RemoveField(
            model_name='item',
            name='unit_plural',
        ),
        migrations.AddField(
            model_name='item',
            name='cost_other',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='cost_shipping',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subitems', to='itemsapp.item'),
        ),
        migrations.AddField(
            model_name='item',
            name='unit_display',
            field=models.ManyToManyField(blank=True, related_name='unit_display', to='itemsapp.UnitDisplay'),
        ),
        migrations.AddField(
            model_name='item',
            name='unit_inventory',
            field=models.ManyToManyField(blank=True, related_name='unit_inventory', to='itemsapp.UnitInventory'),
        ),
    ]
