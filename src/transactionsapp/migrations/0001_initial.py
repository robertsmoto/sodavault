# Generated by Django 3.2 on 2022-02-05 23:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('itemsapp', '0001_initial'),
        ('contactapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(blank=True, choices=[('ASN', 'Advanced Shipping Notice'), ('TRS', 'Transfer'), ('ADJ', 'Inventory Adjustment'), ('ORD', 'Order'), ('RET', 'Return')], max_length=3)),
                ('transaction_number', models.CharField(max_length=100)),
                ('est_shipping_date', models.DateField(blank=True, null=True)),
                ('act_shipping_date', models.DateField(blank=True, null=True)),
                ('est_receiving_date', models.DateField(blank=True, null=True)),
                ('act_receiving_date', models.DateField(blank=True, null=True)),
                ('shipping', models.DecimalField(blank=True, decimal_places=4, help_text='Shipping and handling costs associated with this transaction', max_digits=14, null=True)),
                ('is_complete', models.BooleanField(default=False, help_text='\n            Make sure information in this transaction is correct. \n            Once is_complete is checked, it cannot be unchecked.')),
                ('ship_from_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ship_from_location', to='contactapp.location')),
                ('ship_from_supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ship_from_supplier', to='contactapp.supplier')),
                ('ship_to_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ship_to_location', to='contactapp.location')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_shipped', models.IntegerField(blank=True, help_text='Quantity shipped.', null=True)),
                ('quantity_received', models.IntegerField(blank=True, help_text='Quantity received.', null=True)),
                ('parts', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Parts_TransactionDetails', to='itemsapp.part')),
                ('products', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Products_TransactionDetails', to='itemsapp.product')),
                ('transactions', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='TransactionDetails', to='transactionsapp.transaction')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('note', models.TextField(blank=True, max_length=3000)),
                ('parts', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='note_parts', to='itemsapp.part')),
                ('products', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='note_products', to='itemsapp.product')),
                ('transactions', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='note_asns', to='transactionsapp.transaction')),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_requested', models.DateField(blank=True, null=True)),
                ('date_submitted', models.DateField(blank=True, null=True)),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True)),
                ('shipping', models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True)),
                ('quantity', models.IntegerField(blank=True, default=1, help_text='Divides by this number. 1 box if used by box, or 24 pcs per box if used by piece', null=True)),
                ('units', models.CharField(blank=True, max_length=100)),
                ('is_winning_bid', models.BooleanField(default=False)),
                ('bundle_products', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bid_bundle_products', to='itemsapp.bundleproduct')),
                ('digital_products', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bid_digital_products', to='itemsapp.digitalproduct')),
                ('parts', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bid_parts', to='itemsapp.part')),
                ('products', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bid_products', to='itemsapp.product')),
                ('simple_products', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bid_simple_products', to='itemsapp.simpleproduct')),
                ('suppliers', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bid_suppliers', to='contactapp.supplier')),
                ('variable_products', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bid_variable_products', to='itemsapp.variableproduct')),
            ],
        ),
        migrations.CreateModel(
            name='ASN',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('transactionsapp.transaction',),
        ),
        migrations.CreateModel(
            name='InvAdjustment',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('transactionsapp.transaction',),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('transactionsapp.transaction',),
        ),
        migrations.CreateModel(
            name='Return',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('transactionsapp.transaction',),
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('transactionsapp.transaction',),
        ),
    ]
