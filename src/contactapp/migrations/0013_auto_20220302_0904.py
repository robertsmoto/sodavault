# Generated by Django 3.2 on 2022-03-02 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configapp', '0064_auto_20220302_0904'),
        ('contactapp', '0012_auto_20220302_0853'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={},
        ),
        migrations.RemoveField(
            model_name='company',
            name='address_01',
        ),
        migrations.RemoveField(
            model_name='company',
            name='address_02',
        ),
        migrations.RemoveField(
            model_name='company',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='company',
            name='city',
        ),
        migrations.RemoveField(
            model_name='company',
            name='domain',
        ),
        migrations.RemoveField(
            model_name='company',
            name='id',
        ),
        migrations.RemoveField(
            model_name='company',
            name='name',
        ),
        migrations.RemoveField(
            model_name='company',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='company',
            name='ship_address_01',
        ),
        migrations.RemoveField(
            model_name='company',
            name='ship_address_02',
        ),
        migrations.RemoveField(
            model_name='company',
            name='ship_city',
        ),
        migrations.RemoveField(
            model_name='company',
            name='ship_state',
        ),
        migrations.RemoveField(
            model_name='company',
            name='ship_zipcode',
        ),
        migrations.RemoveField(
            model_name='company',
            name='state',
        ),
        migrations.RemoveField(
            model_name='company',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='company',
            name='website',
        ),
        migrations.RemoveField(
            model_name='company',
            name='zipcode',
        ),
        migrations.AddField(
            model_name='company',
            name='location_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='configapp.location'),
            preserve_default=False,
        ),
    ]
