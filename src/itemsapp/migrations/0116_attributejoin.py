# Generated by Django 3.2 on 2022-02-21 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0115_delete_attributejoin'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeJoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_variation', models.BooleanField(default=False)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('attributes', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attr_join_attributes', to='itemsapp.itemattribute')),
                ('items', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attr_join_items', to='itemsapp.item')),
                ('terms', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attr_join_terms', to='itemsapp.itemattribute')),
            ],
        ),
    ]
