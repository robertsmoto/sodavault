# Generated by Django 3.2 on 2022-02-03 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0026_auto_20220203_0807'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpeningHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.CharField(blank=True, choices=[('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday'), ('SUN', 'Sunday')], max_length=3, verbose_name='Day of Week')),
                ('opens', models.TimeField(blank=True, null=True, verbose_name='Opening Time')),
                ('closes', models.TimeField(blank=True, null=True, verbose_name='Closing Time')),
                ('valid_from', models.DateField(blank=True, help_text='Use for special hours eg. holiday hours', null=True, verbose_name='Valid from')),
                ('valid_to', models.DateField(blank=True, help_text='Use for special hours eg. holiday hours', null=True, verbose_name='Valid to')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Movie title')),
                ('url_item', models.URLField(blank=True, max_length=100, verbose_name='Movie website.')),
                ('url_review', models.URLField(blank=True, help_text='Link to page if there is a full review.', max_length=100, verbose_name='Website full review.')),
                ('language', models.CharField(choices=[('en-GB', 'English United Kingdom'), ('en-IE', 'English Ireland'), ('en-US', 'English United States'), ('cs-CZ', 'Czech Czech Republic'), ('de-DE', 'German Germany'), ('fr-FR', 'French France'), ('it-IT', 'Italian Italy'), ('sk-SK', 'Slovak Slovakia')], default='en-US', max_length=5, verbose_name='Language')),
                ('rating', models.CharField(blank=True, choices=[('1_0', '1.0 worst'), ('1_5', '1.5'), ('2_0', '2.0'), ('2_5', '2.5'), ('3_0', '3.0 average'), ('3_5', '3.5'), ('4_0', '4.0'), ('4_5', '4.5'), ('5_0', '5.0 best')], help_text='5 stars is best.', max_length=3, verbose_name='Rating')),
                ('endorsement', models.CharField(blank=True, choices=[('NOREC', 'Not Recommended'), ('RECOM', 'Recommended')], help_text='Select Recommendation', max_length=5, verbose_name='Endorsement')),
                ('timestamp_created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
