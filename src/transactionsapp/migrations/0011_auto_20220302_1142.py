# Generated by Django 3.2 on 2022-03-02 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contactapp', '0023_auto_20220302_1138'),
        ('transactionsapp', '0010_auto_20220302_1138'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.AddField(
            model_name='asn',
            name='receiver',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='asn_receiver', to='contactapp.location'),
        ),
        migrations.AddField(
            model_name='asn',
            name='sender',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='asn_sender', to='contactapp.location'),
        ),
    ]