# Generated by Django 3.2 on 2022-02-05 23:01

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('configapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name_plural': '03. Attributes',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_type', models.CharField(blank=True, choices=[('CAT', 'Category'), ('TAG', 'Tag'), ('DEP', 'Department')], max_length=3)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('slug', models.SlugField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_type', models.CharField(blank=True, choices=[('PART', 'Part'), ('PROD', 'Product')], max_length=4)),
                ('product_type', models.CharField(blank=True, choices=[('SIMP', 'Simple'), ('DIGI', 'Digital'), ('BUND', 'Bundled'), ('VARI', 'Variable')], max_length=4)),
                ('sku', models.CharField(blank=True, max_length=100)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True, help_text='For internal and purchasing use.')),
                ('ecpu', models.DecimalField(blank=True, decimal_places=4, max_digits=14, null=True)),
                ('ecpu_override', models.DecimalField(blank=True, decimal_places=4, max_digits=14, null=True)),
                ('ecpu_calc_from', models.CharField(blank=True, help_text='how ecpu has been calculated', max_length=100)),
                ('unit', models.CharField(blank=True, help_text='singlular unit', max_length=100)),
                ('unit_override', models.CharField(blank=True, help_text='singlular unit', max_length=100)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ('price_override', models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ('price_calc_from', models.CharField(blank=True, help_text='how price has been calculated', max_length=100)),
                ('price_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='price_items', to='configapp.price')),
            ],
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('slug', models.SlugField()),
                ('img', imagekit.models.fields.ProcessedImageField(blank=True, help_text='converts image to .WebP', null=True, upload_to='product_images/%Y/%m/%d')),
                ('attribute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='terms', to='itemsapp.attribute')),
            ],
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variation_products', to='itemsapp.item')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variation_parents', to='itemsapp.item')),
            ],
        ),
        migrations.CreateModel(
            name='VariationAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attributes', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.attribute')),
                ('items', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.item')),
                ('terms', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.term')),
                ('variations', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variation_attributes', to='itemsapp.variation')),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('slug', models.SlugField()),
                ('begins', models.DateField(null=True)),
                ('ends', models.DateField(null=True)),
                ('percentage', models.DecimalField(decimal_places=2, help_text='Percentage discount eg. 25% off', max_digits=4, null=True)),
                ('fixed', models.DecimalField(decimal_places=2, help_text='Fixed discount eg. $5.00 off', max_digits=8, null=True)),
                ('price', models.DecimalField(decimal_places=2, help_text='Fixed price eg. Sale Price $25.00', max_digits=8, null=True)),
                ('is_free_shipping', models.BooleanField(default=False)),
                ('bogx', models.PositiveSmallIntegerField(help_text='Buy One Get x Free', null=True)),
                ('items', models.ManyToManyField(related_name='promotions', to='itemsapp.Item')),
                ('promotion_override', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='overrides', to='itemsapp.promotion')),
            ],
        ),
        migrations.CreateModel(
            name='ProductAttributeJoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='itemsapp.attribute')),
                ('items', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_att_join', to='itemsapp.item')),
                ('term', models.ManyToManyField(blank=True, to='itemsapp.Term')),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('length', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('width', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('height', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('item', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='measurements', to='itemsapp.item')),
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
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('order', models.IntegerField(blank=True, help_text='integer used to order images', null=True)),
                ('img_lg', imagekit.models.fields.ProcessedImageField(blank=True, help_text='converts to WebP format', null=True, upload_to='product_images/%Y/%m/%d')),
                ('img_md', imagekit.models.fields.ProcessedImageField(blank=True, help_text='converts to WebP format', null=True, upload_to='product_images/%Y/%m/%d')),
                ('img_sm', imagekit.models.fields.ProcessedImageField(blank=True, help_text='converts to WebP format', null=True, upload_to='product_images/%Y/%m/%d')),
                ('img_1x1_lg', imagekit.models.fields.ProcessedImageField(blank=True, help_text='1000px x 1000px', null=True, upload_to='product_images/%Y/%m/%d')),
                ('img_1x1_md', imagekit.models.fields.ProcessedImageField(blank=True, help_text='500px x 500px', null=True, upload_to='product_images/%Y/%m/%d')),
                ('img_1x1_sm', imagekit.models.fields.ProcessedImageField(blank=True, help_text='250px x 250px', null=True, upload_to='product_images/%Y/%m/%d')),
                ('img_2x1_lg', imagekit.models.fields.ProcessedImageField(blank=True, help_text='1000px x 500px', null=True, upload_to='product_images/%Y/%m/%d')),
                ('img_2x1_md', imagekit.models.fields.ProcessedImageField(blank=True, help_text='500px x 250px', null=True, upload_to='product_images/%Y/%m/%d')),
                ('img_2x1_sm', imagekit.models.fields.ProcessedImageField(blank=True, help_text='250px x 125px', null=True, upload_to='product_images/%Y/%m/%d')),
                ('img_1x2_lg', imagekit.models.fields.ProcessedImageField(blank=True, help_text='500px x 1000px', null=True, upload_to='product_images/%Y/%m/%d')),
                ('img_1x2_md', imagekit.models.fields.ProcessedImageField(blank=True, help_text='250px x 500px', null=True, upload_to='product_images/%Y/%m/%d')),
                ('img_1x2_sm', imagekit.models.fields.ProcessedImageField(blank=True, help_text='125px x 250px', null=True, upload_to='product_images/%Y/%m/%d')),
                ('img_16x9', imagekit.models.fields.ProcessedImageField(blank=True, help_text='16:9 1200px x 675px', null=True, upload_to='product_images/%Y/%m/%d')),
                ('img_191x1', imagekit.models.fields.ProcessedImageField(blank=True, help_text='1.91:1 1200px x 628px', null=True, upload_to='product_images/%Y/%m/%d')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='itemsapp.item')),
            ],
            options={
                'ordering': ('order',),
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
                ('item', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='identifiers', to='itemsapp.item')),
            ],
        ),
        migrations.CreateModel(
            name='DigitalOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('item', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='digital_options', to='itemsapp.item')),
            ],
        ),
        migrations.CreateModel(
            name='Bundle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_min', models.PositiveSmallIntegerField(default=1)),
                ('quantity_max', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('is_optional', models.BooleanField(default=False)),
                ('items', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bundle_products', to='itemsapp.item')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bundle_parents', to='itemsapp.item')),
            ],
        ),
        migrations.CreateModel(
            name='BundleProduct',
            fields=[
            ],
            options={
                'verbose_name_plural': '02d. Bundle Products',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('itemsapp.item',),
        ),
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
            bases=('itemsapp.group',),
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
            bases=('itemsapp.group',),
        ),
        migrations.CreateModel(
            name='DigitalProduct',
            fields=[
            ],
            options={
                'verbose_name_plural': '02c. Digital Products',
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
                'verbose_name_plural': '01. Parts',
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
                'verbose_name_plural': '02a. All Products',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('itemsapp.item',),
        ),
        migrations.CreateModel(
            name='SimpleProduct',
            fields=[
            ],
            options={
                'verbose_name_plural': '02b. Simple Products',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('itemsapp.item',),
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
            bases=('itemsapp.group',),
        ),
        migrations.CreateModel(
            name='VariableProduct',
            fields=[
            ],
            options={
                'verbose_name_plural': '02e. Varialbe Products',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('itemsapp.item',),
        ),
        migrations.CreateModel(
            name='ProductPartJoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, help_text='How many parts per product?')),
                ('is_unlimited', models.BooleanField(default=False, help_text='Denotes if a part should be considered unlimited.')),
                ('use_all', models.BooleanField(default=False, help_text='Use all part inventory when the related product is brought into inventory.')),
                ('bundle_products', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ppj_bundle_products', to='itemsapp.bundleproduct')),
                ('digital_products', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ppj_digital_products', to='itemsapp.digitalproduct')),
                ('parts', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ppj_parts', to='itemsapp.part')),
                ('products', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ppj_products', to='itemsapp.product')),
                ('simple_products', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ppj_simple_products', to='itemsapp.simpleproduct')),
                ('variable_products', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ppj_variable_products', to='itemsapp.variableproduct')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='category_items', to='itemsapp.Category'),
        ),
        migrations.AddField(
            model_name='item',
            name='departments',
            field=models.ManyToManyField(blank=True, related_name='department_items', to='itemsapp.Department'),
        ),
        migrations.AddField(
            model_name='item',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tag_item', to='itemsapp.Tag'),
        ),
    ]
