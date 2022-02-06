# Generated by Django 3.2 on 2022-02-06 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_type', models.CharField(blank=True, choices=[('BLOG', 'Blog'), ('LOCA', 'Location'), ('SUPP', 'Suppplier'), ('CUST', 'Customer')], max_length=4)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('phone', models.CharField(blank=True, max_length=200)),
                ('website', models.CharField(blank=True, max_length=200)),
                ('address_01', models.CharField(blank=True, max_length=200)),
                ('address_02', models.CharField(blank=True, max_length=200)),
                ('city', models.CharField(blank=True, max_length=200)),
                ('state', models.CharField(blank=True, max_length=200)),
                ('zipcode', models.CharField(blank=True, max_length=200)),
                ('ship_address_01', models.CharField(blank=True, max_length=200)),
                ('ship_address_02', models.CharField(blank=True, max_length=200)),
                ('ship_city', models.CharField(blank=True, max_length=200)),
                ('ship_state', models.CharField(blank=True, max_length=200)),
                ('ship_zipcode', models.CharField(blank=True, max_length=200)),
            ],
            options={
                'verbose_name_plural': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_type', models.CharField(blank=True, choices=[('CUST', 'Customer'), ('SUPP', 'Suppplier')], max_length=4)),
                ('firstname', models.CharField(blank=True, max_length=200)),
                ('lastname', models.CharField(blank=True, max_length=200)),
                ('nickname', models.CharField(blank=True, max_length=200)),
                ('phone', models.CharField(blank=True, max_length=200)),
                ('mobile', models.CharField(blank=True, max_length=200)),
                ('email', models.CharField(blank=True, max_length=200)),
                ('website', models.CharField(blank=True, max_length=200)),
                ('address_01', models.CharField(blank=True, max_length=200)),
                ('address_02', models.CharField(blank=True, max_length=200)),
                ('city', models.CharField(blank=True, max_length=200)),
                ('state', models.CharField(blank=True, max_length=200)),
                ('zipcode', models.CharField(blank=True, max_length=200)),
                ('ship_address_01', models.CharField(blank=True, max_length=200)),
                ('ship_address_02', models.CharField(blank=True, max_length=200)),
                ('ship_city', models.CharField(blank=True, max_length=200)),
                ('ship_state', models.CharField(blank=True, max_length=200)),
                ('shop_zipcode', models.CharField(blank=True, max_length=200)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contactapp.company')),
            ],
            options={
                'verbose_name_plural': 'people',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('contactapp.company',),
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('contactapp.company',),
        ),
    ]
