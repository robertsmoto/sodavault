# Generated by Django 3.2.3 on 2021-08-23 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='Add Component', max_length=100, verbose_name='Title')),
                ('slug', models.SlugField(help_text='object-action or object-view eg. component-add', verbose_name='Slug')),
                ('url', models.URLField(blank=True, help_text='Link to doc.', verbose_name='URL')),
                ('timestamp_created', models.DateTimeField(blank=True, editable=False, null=True)),
                ('timestamp_modified', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Breadcrumb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text="In last field, use 'title' to use metadata.title, or use_custom_varialbe and coordinate logic with view to use custom name.", max_length=100, verbose_name='Name')),
                ('order', models.IntegerField(blank=True, null=True)),
                ('url_namespace', models.CharField(blank=True, help_text='Must match the URL namespace', max_length=200, verbose_name='URL Namespace')),
                ('url_variables', models.CharField(blank=True, help_text='Variables same as view context eg: comp_pk | part_pk', max_length=200, verbose_name='URL Variables')),
                ('doc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='breadcrumbs', to='docsapp.doc')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
