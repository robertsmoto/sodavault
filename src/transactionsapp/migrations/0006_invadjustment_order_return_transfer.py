from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactionsapp', '0005_auto_20210906_0848'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvAdjustment',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('transactionsapp.transaction',),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('transactionsapp.transaction',),
        ),
        migrations.CreateModel(
            name='Return',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('transactionsapp.transaction',),
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('transactionsapp.transaction',),
        ),
    ]
