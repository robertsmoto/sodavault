# Generated by Django 3.2 on 2022-02-03 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0033_auto_20220203_0913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='book',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blogapp.book'),
        ),
        migrations.AlterField(
            model_name='review',
            name='business',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blogapp.localbusiness'),
        ),
        migrations.AlterField(
            model_name='review',
            name='movie',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blogapp.movie'),
        ),
    ]