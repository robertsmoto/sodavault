# Generated by Django 3.2 on 2022-03-15 14:42

import ckeditor.fields
import configapp.utils.utils_images
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contactapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(help_text='Is required and must be unique.', unique=True)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('kwd_list', models.CharField(blank=True, help_text='Comma-separated values.', max_length=100)),
                ('is_primary', models.BooleanField(default=False)),
                ('is_secondary', models.BooleanField(default=False)),
                ('is_tertiary', models.BooleanField(default=False)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subgroups', to='itemsapp.attribute')),
            ],
            options={
                'verbose_name_plural': '_ attributes',
                'ordering': ['slug'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(help_text='Is required and must be unique.', unique=True)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('kwd_list', models.CharField(blank=True, help_text='Comma-separated values.', max_length=100)),
                ('is_primary', models.BooleanField(default=False)),
                ('is_secondary', models.BooleanField(default=False)),
                ('is_tertiary', models.BooleanField(default=False)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subgroups', to='itemsapp.brand')),
            ],
            options={
                'verbose_name_plural': '_ brands',
                'ordering': ['slug'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(help_text='Is required and must be unique.', unique=True)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('kwd_list', models.CharField(blank=True, help_text='Comma-separated values.', max_length=100)),
                ('is_primary', models.BooleanField(default=False)),
                ('is_secondary', models.BooleanField(default=False)),
                ('is_tertiary', models.BooleanField(default=False)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subgroups', to='itemsapp.category')),
            ],
            options={
                'verbose_name_plural': '__ categories',
                'ordering': ['slug'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CostMultiplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('multiplier_type', models.CharField(blank=True, choices=[('FL', 'Flat Rate'), ('GM', 'Gross Margin'), ('MU', 'Markup')], max_length=4)),
                ('amount', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['multiplier_type', 'amount'],
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(help_text='Is required and must be unique.', unique=True)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('kwd_list', models.CharField(blank=True, help_text='Comma-separated values.', max_length=100)),
                ('is_primary', models.BooleanField(default=False)),
                ('is_secondary', models.BooleanField(default=False)),
                ('is_tertiary', models.BooleanField(default=False)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subgroups', to='itemsapp.department')),
            ],
            options={
                'verbose_name_plural': '_ departments',
                'ordering': ['slug'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_type', models.CharField(choices=[('COMP', 'Component'), ('PART', 'Part'), ('PROD', 'Product')], max_length=4)),
                ('sku', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('description', models.CharField(blank=True, help_text='For internal and purchasing use.', max_length=200)),
                ('keywords', models.CharField(blank=True, help_text='comma, separated, list', max_length=200)),
                ('cost', models.BigIntegerField(default=0)),
                ('cost_shipping', models.BigIntegerField(default=0)),
                ('cost_quantity', models.IntegerField(default=1)),
                ('ecpu', models.BigIntegerField(default=0)),
                ('ecpu_from', models.CharField(blank=True, max_length=20)),
                ('price', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['sku'],
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inv_singular', models.CharField(default='centimeter', max_length=100)),
                ('inv_plural', models.CharField(default='centimeters', max_length=100)),
                ('dis_singular', models.CharField(default='meter', max_length=100)),
                ('dis_plural', models.CharField(default='meters', max_length=100)),
                ('unit_base', models.IntegerField(default=1, help_text='eg. 100 if inventory = 120 cm, display = 1.2 meters')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(help_text='Is required and must be unique.', unique=True)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('kwd_list', models.CharField(blank=True, help_text='Comma-separated values.', max_length=100)),
                ('is_primary', models.BooleanField(default=False)),
                ('is_secondary', models.BooleanField(default=False)),
                ('is_tertiary', models.BooleanField(default=False)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subgroups', to='itemsapp.tag')),
            ],
            options={
                'verbose_name_plural': '__ tags',
                'ordering': ['slug'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('slug', models.SlugField()),
                ('begins', models.DateField(null=True)),
                ('ends', models.DateField(null=True)),
                ('percentage', models.BigIntegerField(blank=True, help_text='Percentage discount eg. 25% off', null=True)),
                ('fixed', models.BigIntegerField(blank=True, help_text='Fixed discount eg. $5.00 off', null=True)),
                ('price', models.BigIntegerField(blank=True, help_text='Fixed price eg. Sale Price $25.00', null=True)),
                ('is_free_shipping', models.BooleanField(default=False)),
                ('bogx', models.PositiveSmallIntegerField(help_text='Buy One Get x Free', null=True)),
                ('item', models.ManyToManyField(blank=True, to='itemsapp.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('note', models.TextField(blank=True, max_length=3000)),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.item')),
            ],
            options={
                'ordering': ['-date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('length', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('width', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('height', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('item', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.item')),
            ],
        ),
        migrations.CreateModel(
            name='Marketing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description_sm', ckeditor.fields.RichTextField(blank=True, help_text='500 characters max.', max_length=500, null=True)),
                ('description_md', ckeditor.fields.RichTextField(blank=True, help_text='1000 characters max.', max_length=1000, null=True)),
                ('description_lg', ckeditor.fields.RichTextField(blank=True, help_text='1000 characters max.', max_length=1000, null=True)),
                ('item', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='marketing_options', to='itemsapp.item')),
            ],
        ),
        migrations.CreateModel(
            name='Ledger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('account', models.CharField(choices=[('APAY', 'Accounts Payable'), ('COGM', 'Cost of Goods Manufactured'), ('COGS', 'Cost of Goods Sold'), ('CASH', 'Cash Account'), ('IRAW', 'Inventory Raw Materials'), ('IMER', 'Inventory Merchandise'), ('ILOS', 'Inventory Loss'), ('OWEQ', 'Owner Equity')], max_length=4)),
                ('date', models.DateField(default=datetime.date.today)),
                ('lot', models.DateTimeField(default=django.utils.timezone.now)),
                ('debit_quantity', models.BigIntegerField(blank=True, null=True)),
                ('debit_amount', models.BigIntegerField(blank=True, null=True)),
                ('credit_quantity', models.BigIntegerField(blank=True, null=True)),
                ('credit_amount', models.BigIntegerField(blank=True, null=True)),
                ('note', models.CharField(blank=True, max_length=200)),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.item')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contactapp.location')),
            ],
            options={
                'verbose_name_plural': 'entries',
            },
        ),
        migrations.CreateModel(
            name='ItemVariationJoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attr_var_join', to='itemsapp.attribute')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_var_join', to='itemsapp.item')),
                ('term', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='term_var_join', to='itemsapp.attribute')),
                ('variation', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='var_var_join', to='itemsapp.item')),
            ],
        ),
        migrations.CreateModel(
            name='ItemCollectionJoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_min', models.IntegerField(default=0, help_text='Use to require minium order quantity.')),
                ('order_max', models.IntegerField(default=0, help_text='Use to limit order quantity.')),
                ('discount', models.IntegerField(default=0, help_text='Discount (5.0%) for purchase in collection.')),
                ('collection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coll_coll_join', to='itemsapp.item')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_coll_join', to='itemsapp.item')),
            ],
        ),
        migrations.CreateModel(
            name='ItemAttributeJoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_variation', models.BooleanField(default=False)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('attribute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attr_attr_join', to='itemsapp.attribute')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_attr_join', to='itemsapp.item')),
                ('terms', models.ManyToManyField(blank=True, related_name='term_attr_join', to='itemsapp.Attribute')),
            ],
        ),
        migrations.CreateModel(
            name='ItemAssemblyJoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, help_text='How many items are included in the cost.')),
                ('is_unlimited', models.BooleanField(default=False, help_text='Is not limited by inventory eg. skilled labor.')),
                ('use_all', models.BooleanField(default=False, help_text='Use the entire quantity when creating a parent item. eg. labels')),
                ('assembly', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assembly_assemb_join', to='itemsapp.item')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_assemb_join', to='itemsapp.item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='assembly',
            field=models.ManyToManyField(blank=True, related_name='_itemsapp_item_assembly_+', through='itemsapp.ItemAssemblyJoin', to='itemsapp.Item'),
        ),
        migrations.AddField(
            model_name='item',
            name='attributes',
            field=models.ManyToManyField(blank=True, through='itemsapp.ItemAttributeJoin', to='itemsapp.Attribute'),
        ),
        migrations.AddField(
            model_name='item',
            name='brands',
            field=models.ManyToManyField(blank=True, to='itemsapp.Brand'),
        ),
        migrations.AddField(
            model_name='item',
            name='categories',
            field=models.ManyToManyField(blank=True, to='itemsapp.Category'),
        ),
        migrations.AddField(
            model_name='item',
            name='collections',
            field=models.ManyToManyField(blank=True, related_name='_itemsapp_item_collections_+', through='itemsapp.ItemCollectionJoin', to='itemsapp.Item'),
        ),
        migrations.AddField(
            model_name='item',
            name='cost_multiplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.costmultiplier'),
        ),
        migrations.AddField(
            model_name='item',
            name='departments',
            field=models.ManyToManyField(blank=True, to='itemsapp.Department'),
        ),
        migrations.AddField(
            model_name='item',
            name='tags',
            field=models.ManyToManyField(blank=True, to='itemsapp.Tag'),
        ),
        migrations.AddField(
            model_name='item',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.unit'),
        ),
        migrations.AddField(
            model_name='item',
            name='variations',
            field=models.ManyToManyField(blank=True, related_name='_itemsapp_item_variations_+', through='itemsapp.ItemVariationJoin', to='itemsapp.Item'),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lg_21', models.ImageField(blank=True, help_text='Recommended size: 2100px x 600px. Recommended name: name-21.jpg', null=True, storage=configapp.utils.utils_images.OverwriteStorage(), upload_to=configapp.utils.utils_images.new_filename)),
                ('lg_11', models.ImageField(blank=True, help_text='Recommended size: 500px x 500px Recommended name: name-11.jpg', null=True, storage=configapp.utils.utils_images.OverwriteStorage(), upload_to=configapp.utils.utils_images.new_filename)),
                ('custom', models.ImageField(blank=True, help_text='Image with custom size.', null=True, storage=configapp.utils.utils_images.OverwriteStorage(), upload_to=configapp.utils.utils_images.new_filename)),
                ('lg_191', models.ImageField(blank=True, help_text='1.9:1 ratio recommended size 2100px x 630px Recommended name: name-191.jpg', null=True, storage=configapp.utils.utils_images.OverwriteStorage(), upload_to=configapp.utils.utils_images.new_filename)),
                ('title', models.CharField(blank=True, help_text='Alt text for image.', max_length=200)),
                ('caption', models.CharField(blank=True, help_text='Caption for image.', max_length=200)),
                ('featured', models.BooleanField(default=False)),
                ('order', models.IntegerField(default=0)),
                ('md_21', models.CharField(blank=True, help_text='Automatic size: 800px x 400px', max_length=200)),
                ('sm_21', models.CharField(blank=True, help_text='Automatic size: 400px x 200px', max_length=200)),
                ('md_11', models.CharField(blank=True, help_text='Automatic size: 250px x 250px', max_length=200)),
                ('sm_11', models.CharField(blank=True, help_text='Automatic size: 200px x 200px', max_length=200)),
                ('category', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.category')),
                ('item', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.item')),
                ('tag', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.tag')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_user_images', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Identifier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid_i', models.BigIntegerField(blank=True, null=True)),
                ('pid_c', models.CharField(blank=True, max_length=100)),
                ('gtin', models.BigIntegerField(blank=True, null=True)),
                ('isbn', models.BigIntegerField(blank=True, null=True)),
                ('item', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.item')),
            ],
        ),
        migrations.CreateModel(
            name='Digital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_int_field', models.BigIntegerField(blank=True, null=True)),
                ('new_char_tield', models.CharField(blank=True, max_length=100)),
                ('item', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.item')),
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
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.item')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contactapp.supplier')),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.unit')),
            ],
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('itemsapp.item',),
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('itemsapp.item',),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('itemsapp.item',),
        ),
        migrations.AddIndex(
            model_name='item',
            index=models.Index(fields=['sku'], name='itemsapp_it_sku_27a3ad_idx'),
        ),
    ]
