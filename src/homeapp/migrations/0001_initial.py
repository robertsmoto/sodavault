# Generated by Django 3.2 on 2022-12-10 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pen_name', models.CharField(blank=True, max_length=100)),
                ('avatar', models.ImageField(blank=True, help_text='Recommended size 250 x 250px', null=True, upload_to='configapp/avatars/%Y/%m/%d')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('location', models.CharField(blank=True, max_length=30)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('cdn_dir', models.CharField(blank=True, help_text='User root cdn dir.eg. https://cdn.sodavault.com/image_dir/Y/m/d/image.webp', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('create_users', 'Can create new users.'), ('view_token', 'Can view token.'), ('change_token', 'Can change token.')],
            },
        ),
        migrations.CreateModel(
            name='APICredentials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aid', models.CharField(default=uuid.uuid4, editable=False, max_length=36)),
                ('auth', models.CharField(default=uuid.uuid4, max_length=36)),
                ('prefix', models.CharField(default=uuid.uuid4, editable=False, max_length=36)),
                ('is_current', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
