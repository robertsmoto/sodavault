# Generated by Django 3.2 on 2022-02-18 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0022_alter_post_websites'),
    ]

    # operations = [
        # migrations.CreateModel(
            # name='Website',
            # fields=[
                # ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # ('name', models.CharField(blank=True, max_length=200)),
                # ('description', models.CharField(blank=True, max_length=200)),
                # ('domain', models.CharField(blank=True, max_length=200, verbose_name='Domain eg. example.com')),
                # ('website', models.CharField(blank=True, max_length=200)),
            # ],
            # options={
                # 'verbose_name_plural': 'locations',
                # 'ordering': ['domain'],
            # },
        # ),
        # migrations.AlterField(
            # model_name='post',
            # name='websites',
            # field=models.ManyToManyField(blank=True, to='blogapp.Website'),
        # ),
    # ]