# Generated by Django 3.2 on 2022-02-25 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configapp', '0024_alter_profile_cdn_dir'),
        ('itemsapp', '0006_auto_20220225_1636'),
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('length', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('width', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('height', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('component', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.component')),
                ('part', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.part')),
                ('product', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.product')),
            ],
        ),
        migrations.CreateModel(
            name='Identifier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid_i', models.BigIntegerField(blank=True, null=True)),
                ('pid_c', models.CharField(blank=True, max_length=100)),
                ('gtin', models.BigIntegerField(blank=True, null=True)),
                ('isbn', models.BigIntegerField(blank=True, null=True)),
                ('product', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.product')),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_requested', models.DateField(blank=True, null=True)),
                ('date_submitted', models.DateField(blank=True, null=True)),
                ('cost', models.BigIntegerField(default=0)),
                ('cost_shipping', models.BigIntegerField(default=0)),
                ('cost_quantity', models.IntegerField(default=1, help_text='Divides total cost by this number to return ecpu.')),
                ('is_winning_bid', models.BooleanField(default=False)),
                ('components', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.component')),
                ('parts', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.part')),
                ('products', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.product')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='configapp.supplier')),
                ('unit_inventory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.unitinventory')),
            ],
        ),
    ]