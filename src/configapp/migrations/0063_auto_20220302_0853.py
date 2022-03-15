# Generated by Django 3.2 on 2022-03-02 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactapp', '0012_auto_20220302_0853'),
        ('itemsapp', '0031_remove_bid_supplier'),
        ('transactionsapp', '0009_auto_20220302_0853'),
        ('blogapp', '0017_auto_20220302_0853'),
        ('configapp', '0062_auto_20220302_0846'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Store',
        ),
        migrations.DeleteModel(
            name='Supplier',
        ),
        migrations.DeleteModel(
            name='Warehouse',
        ),
        migrations.DeleteModel(
            name='Website',
        ),
        migrations.AlterField(
            model_name='profile',
            name='cdn_dir',
            field=models.CharField(default='d6730733-2e88', help_text='User root cdn dir.eg. https://cdn.sodavault.com/image_dir/Y/m/d/image.webp', max_length=20),
        ),
    ]
