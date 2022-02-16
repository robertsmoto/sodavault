# Generated by Django 3.2 on 2022-02-12 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configapp', '0010_unit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('territory', models.CharField(blank=True, max_length=100)),
                ('currency', models.CharField(blank=True, max_length=100)),
                ('symbol', models.CharField(blank=True, max_length=50)),
                ('iso_code', models.CharField(blank=True, max_length=50)),
                ('fractional_unit', models.CharField(blank=True, max_length=50)),
                ('number_basic', models.IntegerField(default=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CurrencyConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('symbol_location', models.CharField(blank=True, max_length=200)),
                ('is_space_separation', models.BooleanField(default=True, help_text='Provides a space between the currency symbol and price.')),
                ('fractional_separator', models.CharField(blank=True, choices=[('DEC', '.'), ('COM', ',')], max_length=3)),
                ('thousands_separator', models.CharField(blank=True, choices=[('DEC', '.'), ('COM', ',')], max_length=3)),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='configapp.currency')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]