# Generated by Django 3.2 on 2022-02-18 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configapp', '0026_group_group_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('domain', models.CharField(blank=True, max_length=200, verbose_name='Domain eg. example.com')),
                ('website', models.CharField(blank=True, max_length=200)),
            ],
            options={
                'verbose_name_plural': 'locations',
                'ordering': ['domain'],
            },
        ),
        migrations.AddField(
            model_name='group',
            name='websites',
            field=models.ManyToManyField(blank=True, to='configapp.Website'),
        ),
    ]