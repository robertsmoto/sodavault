from django import forms
from django_editorjs_fields import EditorJsWidget
from datetime import datetime
from django.forms import ValidationError


class MaxChoiceLengthValidator:
    def __init__(self, max_length):
        self.max_length = max_length

    def __call__(self, value):
        print("######## value", value)
        if len(value) > 0 and len(value[0]) > self.max_length:
            raise ValidationError(
                'Selected choice must be %(max_length)s characters or less.',
                params={'max_length': self.max_length},
            )
        return value


class DocumentForm(forms.Form):
    template_name = 'cmsapp/edit_author.html'

    type = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            # 'readonly': True
        }),
        label='*type:',
        max_length=16,
        required=True,
        help_text="",
    )
    ID = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            # 'readonly': True
        }),
        label='*ID:',
        max_length=16,
        required=True,
        help_text=""
    )
    parentID = forms.CharField(
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        label='parentID:',
        help_text="",
        required=False,
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Needed for internal lists.'}),
        label='*title:',
        max_length=200,
        required=True,
        help_text="",
    )
    description = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Can be used as full text search.'}),
        label='*description:',
        max_length=200,
        required=False,
        help_text="",
    )
    lexi = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            # 'readonly': True,
            'placeholder': 'Automatically generated from docTitle.'
        }),
        label='*lexi:',
        max_length=100,
        required=False,
        help_text="",
    )
    index = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            # 'readonly': True,
            'placeholder': 'Automatically generated on form submit.'
        }),
        label='index:',
        max_length=200,
        required=False,
        help_text="",
    )
    createdAt = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            # 'readonly': True
        }),
        initial=datetime.now(),
        label='*createdAt:',
        required=True,
        help_text="",
    )
    updatedAt = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            # 'readonly': True
        }),
        initial=datetime.now(),
        label='*updatedAt:',
        required=True,
        help_text="",
    )


class AuthorForm(forms.Form):
    firstName = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'prefix': 'author'
        }),
        label='firstName:',
        max_length=100,
        required=False,
        help_text="",
    )
    lastName = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='lastName:',
        max_length=100,
        required=False,
        help_text="",
    )
    penName = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='penName:',
        max_length=100,
        required=False,
        help_text="",
    )
    role = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label='role:',
        help_text="",
        required=False,
        choices=[
            ('', 'choose ...'),
            ('author', 'Author'),
            ('editor', 'Editor'),
            ('publisher', 'Publisher'),
        ]
    )


class WebsiteForm(forms.Form):
    websiteDomain = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='websiteDomain:',
        max_length=100,
        help_text="",
    )
    websiteUrl = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='websiteUrl:',
        max_length=100,
        help_text="",
    )


class IngredientForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Name',
        }),
        label='Name:',
        help_text="",
        required=False,
        max_length=50,
    )
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Qnty',
        }),
        label='Quantity:',
        help_text="",
        required=False,
        min_value=0,
    )
    unit = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Unit',
        }),
        label='Unit:',
        help_text="",
        required=False,
        max_length=20,
    )
    note = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Note',
        }),
        label='Note:',
        help_text="",
        required=False,
        max_length=50,
    )


class NutritionForm(forms.Form):
    # nutrition
    servingSize = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Serving Size (eg. 150g)'
        }),
        label='ServingSize:',
        max_length=50,
        required=False,
        help_text="",
    )
    calories = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Total Calories'
        }),
        label='Calories:',
        min_value=0,
        required=False,
        help_text="",
    )
    fatContent = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Total Fat (grams)'
        }),
        label='FatContent:',
        min_value=0,
        required=False,
        help_text="",
    )
    saturatedFat = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Saturated Fat (grams)'
        }),
        label='SaturatedFat:',
        min_value=0,
        required=False,
        help_text="",
    )
    unsaturatedFat = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Unsaturated Fat (grams)'
        }),
        label='UnsaturatedFat:',
        min_value=0,
        required=False,
        help_text="",
    )
    transFat = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Trans Fat (grams)'
        }),
        label='TransFat:',
        min_value=0,
        required=False,
        help_text="",
    )
    cholesterolContent = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cholesterol (milligrams)'
        }),
        label='CholesterolContent:',
        min_value=0,
        required=False,
        help_text="",
    )
    sodiumContent = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sodium (milligrams)'
        }),
        label='SodiumContent:',
        min_value=0,
        required=False,
        help_text="",
    )
    carbohydrateContent = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Carbohydrats (grams)'
        }),
        label='CarbohydrateContent:',
        min_value=0,
        required=False,
        help_text="",
    )
    fiberContent = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Fiber (grams)'
        }),
        label='FiberContent:',
        min_value=0,
        required=False,
        help_text="",
    )
    sugarContent = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sugar (grams)'
        }),
        label='SugarContent:',
        min_value=0,
        required=False,
        help_text="",
    )
    proteinContent = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Protein (grams)'
        }),
        label='ProteinContent:',
        min_value=0,
        required=False,
        help_text="",
    )


class RecipeForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Recipe Name (eg. Apple Pie)',
        }),
        label='Name:',
        required=False,
        max_length=100,
        help_text="",
    )
    yieldQuantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Quantitiy',
        }),
        label='YieldQuantity:',
        required=False,
        min_value=0,
        help_text="",
    )
    yieldDescription = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Description (eg. 200g per serving)',
        }),
        label='YieldDescription:',
        required=False,
        max_length=50,
        help_text="",
    )
    yieldNote = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Note',
        }),
        label='YieldNote:',
        required=False,
        max_length=100,
        help_text="",
    )
    # prep time
    prepTimeHours = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label='PrepTimeHours:',
        help_text="",
        required=False,
        choices=[
            ('', 'choose hours ...'),
            ('0', '0 hours'),
            ('1', '1 hours'),
            ('2', '2 hours'),
            ('3', '3 hours'),
            ('4', '4 hours'),
            ('5', '5 hours'),
            ('6', '6 hours'),
            ('7', '7 hours'),
            ('8', '8 hours'),
            ('9', '9 hours'),
            ('10', '10 hours'),
            ('11', '11 hours'),
            ('12', '12 hours'),
            ('13', '13 hours'),
            ('14', '14 hours'),
            ('15', '15 hours'),
            ('16', '16 hours'),
            ('17', '17 hours'),
            ('18', '18 hours'),
            ('19', '19 hours'),
            ('20', '20 hours'),
            ('21', '21 hours'),
            ('22', '22 hours'),
            ('23', '23 hours')
        ]
    )
    prepTimeMinutes = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label='PrepTimeMinutes:',
        help_text="",
        required=False,
        choices=[
            ('', 'choose minutes ...'),
            ('0', '0 minutes'),
            ('5', '5 minutes'),
            ('10', '10 minutes'),
            ('15', '15 minutes'),
            ('20', '20 minutes'),
            ('25', '25 minutes'),
            ('30', '30 minutes'),
            ('35', '35 minutes'),
            ('40', '40 minutes'),
            ('45', '45 minutes'),
            ('50', '50 minutes'),
            ('55', '55 minutes')
        ]
    )
    # cook time
    cookTimeHours = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label='CookTimeHours:',
        help_text="",
        required=False,
        choices=[
            ('', 'choose hours ...'),
            ('0', '0 hours'),
            ('1', '1 hours'),
            ('2', '2 hours'),
            ('3', '3 hours'),
            ('4', '4 hours'),
            ('5', '5 hours'),
            ('6', '6 hours'),
            ('7', '7 hours'),
            ('8', '8 hours'),
            ('9', '9 hours'),
            ('10', '10 hours'),
            ('11', '11 hours'),
            ('12', '12 hours'),
            ('13', '13 hours'),
            ('14', '14 hours'),
            ('15', '15 hours'),
            ('16', '16 hours'),
            ('17', '17 hours'),
            ('18', '18 hours'),
            ('19', '19 hours'),
            ('20', '20 hours'),
            ('21', '21 hours'),
            ('22', '22 hours'),
            ('23', '23 hours')
        ]
    )
    cookTimeMinutes = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label='CookTimeMinutes:',
        help_text="",
        required=False,
        choices=[
            ('', 'choose minutes ...'),
            ('0', '0 minutes'),
            ('5', '5 minutes'),
            ('10', '10 minutes'),
            ('15', '15 minutes'),
            ('20', '20 minutes'),
            ('25', '25 minutes'),
            ('30', '30 minutes'),
            ('35', '35 minutes'),
            ('40', '40 minutes'),
            ('45', '45 minutes'),
            ('50', '50 minutes'),
            ('55', '55 minutes')
        ]
    )


class BookReview(forms.Form):
    book_title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='book_title:',
        max_length=200,
        required=False,
        help_text="",
    )
    book_isbn = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='book_isbn:',
        max_length=13,
        required=False,
        help_text="",
    )
    book_author = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='book_author:',
        max_length=200,
        required=False,
        help_text="",
    )
    book_authorUrl = forms.URLField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='book_authorUrl:',
        max_length=200,
        required=False,
        help_text="",
    )
    book_language = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='book_language:',
        max_length=200,
        required=False,
        help_text="",
    )
    book_negativeNotes = forms.CharField(
        widget=EditorJsWidget(
            config=None,
            plugins=None,
            tools=None,
        ),
        label='book_negativeNotes:',
        required=False,
    )
    book_positiveNotes = forms.CharField(
        widget=EditorJsWidget(
            config=None,
            plugins=None,
            tools=None,
        ),
        label='book_positiveNotes:',
        required=False,
    )


class LocalBusinessReview(forms.Form):

    business_type = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='business_type:',
        max_length=200,
        required=False,
        help_text="",
    )
    business_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='business_name:',
        max_length=200,
        required=False,
        help_text="",
    )
    business_address_street = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='business_address_street:',
        max_length=200,
        required=False,
        help_text="",
    )
    business_address_city = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='business_address_city:',
        max_length=200,
        required=False,
        help_text="",
    )
    business_address_state = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='business_address_state:',
        max_length=200,
        required=False,
        help_text="",
    )
    business_address_zipCode = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='business_address_zipCode:',
        max_length=200,
        required=False,
        help_text="",
    )
    business_address_country = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='business_address_country:',
        max_length=200,
        required=False,
        help_text="",
    )
    business_phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='business_phone:',
        max_length=200,
        required=False,
        help_text="",
    )
    business_website = forms.URLField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='business_website:',
        max_length=200,
        required=False,
        help_text="",
    )
    business_mapLink = forms.URLField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='business_mapLink:',
        max_length=200,
        required=False,
        help_text="",
    )
    business_latitude = forms.FloatField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='business_latitude:',
        required=False,
        help_text="",
    )
    business_longitude = forms.FloatField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='business_longitude:',
        required=False,
        help_text="",
    )
    business_negativeNotes = forms.CharField(
        widget=EditorJsWidget(
            config=None,
            plugins=None,
            tools=None,
        ),
        label='business_negativeNotes:',
        required=False,
    )
    business_positiveNotes = forms.CharField(
        widget=EditorJsWidget(
            config=None,
            plugins=None,
            tools=None,
        ),
        label='business_positiveNotes:',
        required=False,
    )
    business_restaurant_menu = forms.URLField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='business_restaurant_menu:',
        max_length=200,
        required=False,
        help_text="",
    )
    business_restaurant_type = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'eg. Fast Food, Fine Dining'
        }),
        label='business_restaurant_type:',
        max_length=200,
        required=False,
        help_text="",
    )
    business_restaurant_cuisine = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'eg. Italian, French'
        }),
        label='business_restaurant_cuisine:',
        max_length=200,
        required=False,
        help_text="",
    )
    business_restaurant_acceptsReservations = forms.BooleanField(
        # widget=forms.CheckboxInput(attrs={
        # 'class': 'form-control',
        # }),
        label='business_restaurant_acceptsReservations:',
        required=False,
        help_text="",
    )
    business_restaurant_cost = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label='business_restaurant_cost:',
        help_text="",
        required=False,
        choices=[
            ('', 'choose ...'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3')
        ]
    )


class MovieReview(forms.Form):
    pass


class Rating(forms.Form):
    rating_value = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label='rating_value:',
        help_text="",
        required=False,
        choices=[
            ('', 'choose ...'),
            ('1', '1'),
            ('1.5', '1.5'),
            ('2', '2'),
            ('2.5', '2.5'),
            ('3', '3'),
            ('3.5', '3.5'),
            ('4', '4'),
            ('4.5', '4.5'),
            ('5', '5'),
        ]
    )


class Endorsement(forms.Form):
    endorsement_ratingValue = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label='endorsement_ratingValue:',
        help_text="",
        required=False,
        choices=[
            ('', 'choose ...'),
            ('1', '1'),
            ('1.5', '1.5'),
            ('2', '2'),
            ('2.5', '2.5'),
            ('3', '3'),
            ('3.5', '3.5'),
            ('4', '4'),
            ('4.5', '4.5'),
            ('5', '5')
        ]
    )
    endorsement_ratingExplanation = forms.CharField(
        widget=EditorJsWidget(
            config=None,
            plugins=None,
            tools=None,
        ),
        label='endorsement_ratingExplanation:',
        required=False,
    )


class ArticleForm(forms.Form):
    # attributes
    headline = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='headline:',
        max_length=200,
        required=False,
        help_text="",
    )
    subHeadline = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label='subHeadline:',
        max_length=200,
        required=False,
        help_text="",
    )
    body = forms.CharField(
        widget=EditorJsWidget(config={
            'minHeight': 100
        }),
        required=False,
        label='body:',
    )
    excerpt = forms.CharField(
        widget=EditorJsWidget(config={
            'minHeight': 100
        }),
        required=False,
        label='excerpt:',
    )
    footer = forms.CharField(
        widget=EditorJsWidget(config={}),
        required=False,
        label='footer:',
    )


class AuthorCollectionForm(forms.Form):

    author = forms.CharField(
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
        }),
        label='author:',
        help_text="",
        required=False,
    )


class WebsiteCollectionForm(forms.Form):

    website = forms.CharField(
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
        }),
        label='website:',
        help_text="",
        required=False,
    )


class RecipeCollectionForm(forms.Form):

    recipeCookingMethod = forms.CharField(
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
        }),
        label='recipeCookingMethod:',
        help_text="",
        required=False,
    )
    recipeCuisine = forms.CharField(
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
        }),
        label='recipeCuisine:',
        help_text="",
        required=False,
    )
    recipeCategory = forms.CharField(
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
        }),
        label='recipeCategory:',
        help_text="",
        required=False,
    )
    recipeSuitableForDiet = forms.CharField(
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
        }),
        label='recipeSuitableForDiet:',
        help_text="",
        required=False,
    )


class ArticleCollectionForm(AuthorCollectionForm, WebsiteCollectionForm,
                            RecipeCollectionForm):

    # articleCollections
    articleCategory = forms.CharField(
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
        }),
        label='articleCategories:',
        help_text="",
        required=False,
    )
    articleKeyword = forms.CharField(
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
        }),
        label='articleKeywords:',
        help_text="",
        required=False,
    )
    articleTag = forms.CharField(
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
        }),
        label='articleTags:',
        help_text="",
        required=False,
    )

    articleStatus = forms.CharField(
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            },
            choices=[
                ('draft', 'Draft'),
                ('review', 'Review'),
                ('published', 'Published'),
            ]

        ),
        label='articleStatus:',
        help_text="",
        required=False,
    )
    articleHighlight = forms.CharField(
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            },
            choices=[
                ('', 'choose ...'),
                ('featured', 'isFeatured'),
                ('sticky', 'isSticky'),
                ('promoted', 'isPromoted'),
            ]
        ),
        label='articleHighlight:',
        help_text="",
        required=False,
        # choices=[
        # ('featured', 'isFeatured'),
        # ('sticky', 'isSticky'),
        # ('promoted', 'isPromoted'),
        # ]
    )
