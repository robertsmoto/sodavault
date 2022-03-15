# Generated by Django 3.2 on 2022-02-27 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0010_remove_image_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='category',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog_category_images', to='blogapp.category'),
        ),
        migrations.AlterField(
            model_name='image',
            name='tag',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog_tag_images', to='blogapp.tag'),
        ),
    ]