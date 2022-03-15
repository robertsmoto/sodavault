# Generated by Django 3.2 on 2022-03-01 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('itemsapp', '0025_rename_variation_productvariationjoin'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='variations',
            field=models.ManyToManyField(blank=True, related_name='_itemsapp_product_variations_+', through='itemsapp.ProductVariationJoin', to='itemsapp.Product'),
        ),
        migrations.AddField(
            model_name='productvariationjoin',
            name='variations',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variation_pvj', to='itemsapp.product'),
        ),
        migrations.AlterField(
            model_name='productvariationjoin',
            name='attribute',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attribute_pvj', to='itemsapp.attribute'),
        ),
        migrations.AlterField(
            model_name='productvariationjoin',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_pvj', to='itemsapp.product'),
        ),
        migrations.AlterField(
            model_name='productvariationjoin',
            name='term',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='term_pvj', to='itemsapp.attribute'),
        ),
    ]