# Generated by Django 3.2 on 2022-03-15 14:42

import ckeditor_uploader.fields
import configapp.utils.utils_images
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contactapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Book title')),
                ('isbn', models.CharField(blank=True, max_length=13, verbose_name='ISBN')),
                ('author', models.CharField(blank=True, help_text='Author of book.', max_length=100, null=True, verbose_name='Book Author')),
                ('author_url', models.URLField(blank=True, help_text='Website or wiki of Book Author.', max_length=100, verbose_name='Link to Book Author')),
                ('url_book', models.URLField(blank=True, help_text='Website of item being reviewed.', max_length=100, verbose_name='Link to book.')),
                ('language', models.CharField(choices=[('en-GB', 'English United Kingdom'), ('en-IE', 'English Ireland'), ('en-US', 'English United States'), ('cs-CZ', 'Czech Czech Republic'), ('de-DE', 'German Germany'), ('fr-FR', 'French France'), ('it-IT', 'Italian Italy'), ('sk-SK', 'Slovak Slovakia')], default='en-US', max_length=5, verbose_name='Language')),
                ('cost', models.CharField(blank=True, choices=[('FREE', 'Free'), ('CHEA', 'Cheap'), ('MODE', 'Moderate'), ('EXPE', 'Expensive')], help_text='How expensive?', max_length=4, verbose_name='Cost')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(help_text='Is required and must be unique.', unique=True)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('kwd_list', models.CharField(blank=True, help_text='Comma-separated values.', max_length=100)),
                ('is_primary', models.BooleanField(default=False)),
                ('is_secondary', models.BooleanField(default=False)),
                ('is_tertiary', models.BooleanField(default=False)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subgroups', to='blogapp.category')),
            ],
            options={
                'verbose_name_plural': '__ categories',
                'ordering': ['slug'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LocalBusiness',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus_type', models.CharField(blank=True, help_text="Be specific eg. Restaurant, see schema.org 'types'", max_length=200, verbose_name='Business Type')),
                ('name', models.CharField(blank=True, max_length=200, verbose_name='Business name')),
                ('address_street', models.CharField(blank=True, max_length=100, verbose_name='Street Address')),
                ('address_city', models.CharField(blank=True, max_length=100, verbose_name='City')),
                ('address_state', models.CharField(blank=True, help_text='state or province', max_length=100, verbose_name='State')),
                ('address_zipcode', models.CharField(blank=True, max_length=20, verbose_name='Zip Code')),
                ('address_country', models.CharField(choices=[('AT', 'Austria'), ('CZ', 'Czech Republic'), ('DE', 'Germany'), ('FR', 'France'), ('IT', 'Italy'), ('SK', 'Slovakia'), ('US', 'United States of America')], default='CZ', max_length=2, verbose_name='Country')),
                ('phone', models.CharField(blank=True, help_text='Including country code, only for businesses.', max_length=20, verbose_name='Phone Number')),
                ('website', models.URLField(blank=True, help_text='Use google maps link.', max_length=100, verbose_name='Business website.')),
                ('map_link', models.URLField(blank=True, help_text='Use google maps link.', max_length=100, verbose_name='Map link.')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=8, null=True, verbose_name='Latitude')),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=8, null=True, verbose_name='Longitude')),
                ('restaurant_menu', models.URLField(blank=True, help_text='Link to menu for restaurants.', max_length=100, verbose_name='Menu')),
                ('restaurant_type', models.CharField(blank=True, choices=[('CASU', 'Casual Dining'), ('FINE', 'Fine Dining'), ('FAST', 'Fast Service')], max_length=4, verbose_name='Restaurant Type')),
                ('restaurant_cuisine', models.CharField(blank=True, help_text='Cuisine', max_length=100, verbose_name='Cuisine Offered.')),
                ('restaurant_reservations', models.BooleanField(default=False, help_text='Does the restaurant accept reservations?', verbose_name='Accepts Reservations')),
                ('price_range', models.CharField(blank=True, choices=[('FREE', 'Free'), ('CHEA', 'Cheap'), ('MODE', 'Moderate'), ('EXPE', 'Expensive')], help_text='How expensive?', max_length=4, verbose_name='Price Range')),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Movie title')),
                ('url_item', models.URLField(blank=True, max_length=100, verbose_name='Movie website.')),
                ('language', models.CharField(choices=[('en-GB', 'English United Kingdom'), ('en-IE', 'English Ireland'), ('en-US', 'English United States'), ('cs-CZ', 'Czech Czech Republic'), ('de-DE', 'German Germany'), ('fr-FR', 'French France'), ('it-IT', 'Italian Italy'), ('sk-SK', 'Slovak Slovakia')], default='en-US', max_length=5, verbose_name='Language')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Name of dish.', max_length=100, verbose_name='Name')),
                ('prep_time', models.IntegerField(blank=True, help_text='Time in minutes. eg. 30', null=True, verbose_name='Prep Time')),
                ('cook_time', models.IntegerField(blank=True, help_text='Time in minutes. eg. 45', null=True, verbose_name='Cook Time')),
                ('instructions', models.TextField(blank=True, help_text='In a large bowl ...', verbose_name='Instructions')),
                ('recipe_yield_qnty', models.IntegerField(blank=True, help_text='eg. 25', null=True, verbose_name='Yield Qnty')),
                ('recipe_yield_description', models.CharField(blank=True, help_text='eg. cookies, loaf, servings', max_length=50, verbose_name='Yield Description')),
                ('recipe_yield_notes', models.CharField(blank=True, help_text='eg. Cookies approx. size 25 grams.', max_length=50, verbose_name='Yield Notes')),
                ('cooking_method', models.CharField(blank=True, help_text='eg. Frying, Steaming, Baking.', max_length=50, verbose_name='Cooking method')),
                ('category', models.CharField(blank=True, help_text='eg. Entree, Appetizer, Side.', max_length=50, verbose_name='Category')),
                ('cuisine', models.CharField(blank=True, help_text='eg. Italian, French, American.', max_length=50, verbose_name='Cuisine')),
                ('suitable', models.CharField(blank=True, help_text='Restricted Diet eg. Vegan.', max_length=50, verbose_name='Suitable for')),
                ('nutr_serving', models.CharField(blank=True, help_text='10 gram slice', max_length=50, verbose_name='Serving Size')),
                ('nutr_calories', models.CharField(blank=True, help_text='100', max_length=10, verbose_name='Number of calories per serving.')),
                ('nutr_carbs', models.CharField(blank=True, help_text='100', max_length=10, verbose_name='Grams of carbohydrates per serving.')),
                ('nutr_choles', models.CharField(blank=True, help_text='100', max_length=10, verbose_name='Milligrams of cholesterol per serving.')),
                ('nutr_fat', models.CharField(blank=True, help_text='100', max_length=10, verbose_name='Grams of fat per serving.')),
                ('nutr_fiber', models.CharField(blank=True, help_text='100', max_length=10, verbose_name='Grams of fiber per serving.')),
                ('nutr_protein', models.CharField(blank=True, help_text='100', max_length=10, verbose_name='Grams of protein per serving.')),
                ('nutr_sat_fat', models.CharField(blank=True, help_text='100', max_length=10, verbose_name='Grams of staurated fat per serving.')),
                ('nutr_sodium', models.CharField(blank=True, help_text='100', max_length=10, verbose_name='Milligrams of sodium per serving.')),
                ('nutr_sugar', models.CharField(blank=True, help_text='100', max_length=10, verbose_name='Grams of sugar per serving.')),
                ('nutr_trans_fat', models.CharField(blank=True, help_text='100', max_length=10, verbose_name='Grams of trans fat per serving.')),
                ('nutr_unsat_fat', models.CharField(blank=True, help_text='100', max_length=10, verbose_name='Grams of unstaurated fat per serving.')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(help_text='Is required and must be unique.', unique=True)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('kwd_list', models.CharField(blank=True, help_text='Comma-separated values.', max_length=100)),
                ('is_primary', models.BooleanField(default=False)),
                ('is_secondary', models.BooleanField(default=False)),
                ('is_tertiary', models.BooleanField(default=False)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subgroups', to='blogapp.tag')),
            ],
            options={
                'verbose_name_plural': '__ tags',
                'ordering': ['slug'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(blank=True, choices=[('1_0', '1.0 worst'), ('1_5', '1.5'), ('2_0', '2.0'), ('2_5', '2.5'), ('3_0', '3.0 average'), ('3_5', '3.5'), ('4_0', '4.0'), ('4_5', '4.5'), ('5_0', '5.0 best')], help_text='5 stars is best.', max_length=3, verbose_name='Rating')),
                ('endorsement', models.CharField(blank=True, choices=[('NOREC', 'Not Recommended'), ('RECOM', 'Recommended')], help_text='Select Recommendation', max_length=5, verbose_name='Endorsement')),
                ('book', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blogapp.book')),
                ('business', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blogapp.localbusiness')),
                ('movie', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blogapp.movie')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_type', models.CharField(blank=True, choices=[('ARTI', 'Article'), ('DOCU', 'Documentation'), ('PAGE', 'Page')], max_length=4)),
                ('slug', models.SlugField(help_text='Is required, must be unique.', unique=True)),
                ('title', models.CharField(blank=True, max_length=200, verbose_name='Title')),
                ('excerpt', ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='Max 200 characters.', max_length=200, null=True)),
                ('body', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('PUBLI', 'Published'), ('DRAFT', 'Draft'), ('TRASH', 'Trash')], max_length=5, verbose_name='Status')),
                ('is_featured', models.BooleanField(default=False, help_text='Moves post to front page.', verbose_name='Featured Post')),
                ('menu_order', models.IntegerField(default=0, help_text='Use to order menu', verbose_name='Menu Order')),
                ('is_primary', models.BooleanField(default=False, help_text='Use if in primary menu.')),
                ('is_secondary', models.BooleanField(default=False, help_text='Use if in secondary menu.')),
                ('is_tertiary', models.BooleanField(default=False, help_text='Use if in footer menu.')),
                ('date_published', models.DateField(default=datetime.date.today, verbose_name='Date Published')),
                ('date_modified', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Date Modified')),
                ('kwd_list', models.CharField(blank=True, help_text='Comma-separated list', max_length=200, verbose_name='Keyword List')),
                ('footer', ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='Use for footnotes, redactions and notes of changes or updates.', null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('book', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blogapp.book')),
                ('categories', models.ManyToManyField(blank=True, to='blogapp.Category')),
                ('local_business', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blogapp.localbusiness')),
                ('movie', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blogapp.movie')),
                ('parent', models.ForeignKey(blank=True, help_text='Self-referencing field to nest menus.', null=True, on_delete=django.db.models.deletion.CASCADE, to='blogapp.post')),
                ('recipe', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blogapp.recipe')),
                ('tags', models.ManyToManyField(blank=True, to='blogapp.Tag')),
                ('websites', models.ManyToManyField(blank=True, to='contactapp.Website')),
            ],
            options={
                'ordering': ('-is_featured', '-date_published'),
            },
        ),
        migrations.CreateModel(
            name='OpeningHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.CharField(blank=True, choices=[('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday'), ('SUN', 'Sunday')], max_length=3, verbose_name='Day of Week')),
                ('opens', models.TimeField(blank=True, null=True, verbose_name='Opening Time')),
                ('closes', models.TimeField(blank=True, null=True, verbose_name='Closing Time')),
                ('valid_from', models.DateField(blank=True, help_text='Use for special hours eg. holiday hours', null=True, verbose_name='Valid from')),
                ('valid_to', models.DateField(blank=True, help_text='Use for special hours eg. holiday hours', null=True, verbose_name='Valid to')),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogapp.localbusiness')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(blank=True, help_text='Weight in grams. eg. 50', null=True, verbose_name='Weight (grams)')),
                ('name', models.CharField(blank=True, help_text='ex. white onion, celery, pasta', max_length=100, verbose_name='Ingredient')),
                ('notes', models.CharField(blank=True, help_text='ex. finely chopped', max_length=200, verbose_name='Note')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogapp.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lg_21', models.ImageField(blank=True, help_text='Recommended size: 2100px x 600px. Recommended name: name-21.jpg', null=True, storage=configapp.utils.utils_images.OverwriteStorage(), upload_to=configapp.utils.utils_images.new_filename)),
                ('lg_11', models.ImageField(blank=True, help_text='Recommended size: 500px x 500px Recommended name: name-11.jpg', null=True, storage=configapp.utils.utils_images.OverwriteStorage(), upload_to=configapp.utils.utils_images.new_filename)),
                ('custom', models.ImageField(blank=True, help_text='Image with custom size.', null=True, storage=configapp.utils.utils_images.OverwriteStorage(), upload_to=configapp.utils.utils_images.new_filename)),
                ('lg_191', models.ImageField(blank=True, help_text='1.9:1 ratio recommended size 2100px x 630px Recommended name: name-191.jpg', null=True, storage=configapp.utils.utils_images.OverwriteStorage(), upload_to=configapp.utils.utils_images.new_filename)),
                ('title', models.CharField(blank=True, help_text='Alt text for image.', max_length=200)),
                ('caption', models.CharField(blank=True, help_text='Caption for image.', max_length=200)),
                ('featured', models.BooleanField(default=False)),
                ('order', models.IntegerField(default=0)),
                ('md_21', models.CharField(blank=True, help_text='Automatic size: 800px x 400px', max_length=200)),
                ('sm_21', models.CharField(blank=True, help_text='Automatic size: 400px x 200px', max_length=200)),
                ('md_11', models.CharField(blank=True, help_text='Automatic size: 250px x 250px', max_length=200)),
                ('sm_11', models.CharField(blank=True, help_text='Automatic size: 200px x 200px', max_length=200)),
                ('category', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog_category_images', to='blogapp.category')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blogapp.post')),
                ('tag', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog_tag_images', to='blogapp.tag')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog_user_images', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('blogapp.post',),
        ),
        migrations.CreateModel(
            name='Doc',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('blogapp.post',),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('blogapp.post',),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['status', 'date_published', 'is_featured'], name='blogapp_pos_status_a16a35_idx'),
        ),
    ]
