# Generated by Django 3.2 on 2022-03-02 12:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('transactionsapp', '0011_auto_20220302_1142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asn',
            name='onboarding_cost',
        ),
        migrations.AddField(
            model_name='asn',
            name='other_cost',
            field=models.BigIntegerField(default=0, help_text='Record other related costs here such as onboarding costs.'),
        ),
        migrations.AlterField(
            model_name='asn',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='asn',
            name='number',
            field=models.CharField(default='ASN-2022-03-02', max_length=100),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='number',
            field=models.CharField(default='ASN-2022-03-02', max_length=100),
        ),
    ]
