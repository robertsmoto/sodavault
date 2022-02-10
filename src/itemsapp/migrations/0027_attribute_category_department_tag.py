# Generated by Django 3.2 on 2022-02-10 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configapp', '0005_group'),
        ('itemsapp', '0026_auto_20220210_0904'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
            ],
            options={
                'verbose_name_plural': '05. Categories',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('configapp.group',),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
            ],
            options={
                'verbose_name_plural': '04. Departments',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('configapp.group',),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
            ],
            options={
                'verbose_name_plural': '06. Tags',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('configapp.group',),
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='configapp.group')),
                ('new_field', models.CharField(blank=True, max_length=200)),
                ('terms', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.attribute')),
            ],
            options={
                'verbose_name_plural': '07. Attributes',
            },
            bases=('configapp.group',),
        ),
    ]
