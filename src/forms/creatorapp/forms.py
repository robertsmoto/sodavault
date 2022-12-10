from ckeditor.widgets import CKEditorWidget
from crispy_forms.bootstrap import Div, Tab, TabHolder, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Submit, Button
from django import forms
from svapi_py.api import SvApi

class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('title', wrapper_class='col-md-8'),
                Field('slug', wrapper_class='col-md-4'),
                css_class='row mt-2',
                ),
            Div(
                Field('createdAt', wrapper_class='col-md-4'),
                Field('id', wrapper_class='col-md-4'),
                Field('parentId', wrapper_class='col-md-4'),
                css_class='row mt-2'
                ),
            Div(
                Field('status', wrapper_class='col-md-auto'),
                Field('highlight', wrapper_class='col-md-auto'),
                Field('location', wrapper_class='col-md-auto'),
                Field('position', wrapper_class='col-md-auto'),
                Field('type', wrapper_class='col-md-auto'),
                css_class='row mt-2',
                ),
            Div(
                TabHolder(
                    Tab('Body',
                        Div(
                            'body',
                            css_class='row'
                            )
                        ),
                    Tab('Excerpt',
                        Div(
                            'excerpt',
                            css_class='row'
                            )
                        ),
                    Tab('Footer',
                        Div(
                            'footer',
                            css_class='row'
                            )
                        )
                    ),
                css_class='mt-3'
                ),
            FormActions(
                Submit('save', 'Save changes'),
                Button('cancel', 'Cancel')
                ),
        )


    STATUS_CHOICES = [
            ('draft', 'draft'),
            ('review', 'review'),
            ('published', 'published'),
            ]
    HIGHLIGHT_CHOICES = [
            ('', '----'),
            ('isFeatured', 'isFeatured'),
            ('isPromoted', 'isPromoted'),
            ('isSticky', 'isSticky'),
            ]
    MENU_CHOICES=[
            ('', '----'),
            ('isPrimary','isPrimary'),
            ('isSecondary','isSecondary'),
            ('isTeriary','isTertiary'),
            ]

    # p_qdata = [QueryData(alias='pages', typeArg='page')]
    # pages = Query('all_pages', p_qdata).queryset()
    # PARENT_CHOICES = [(x['id'], x['title']) for x in pages]
    # PARENT_CHOICES.insert(0, ('', '----'))

    PARENT_CHOICES = [("AA", "aa"),]


    id = forms.CharField(label='id')
    parentId = forms.ChoiceField(
            required=False,
            label='parent',
            choices=PARENT_CHOICES
            )
    type = forms.CharField(disabled=True, label='type')
    createdAt = forms.DateTimeField(
            required=False,
            label='createdAt',
            widget=forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
                )
            )
    # widgets = {'createdAt': DateTimePicerInput}
    title = forms.CharField(required=False, label='title')
    slug = forms.CharField(required=False, label='slug')
    status = forms.ChoiceField(
            choices=STATUS_CHOICES,
            required=False,
            label='status'
            )

    position = forms.IntegerField(required=False, label='menuPosition')
    location = forms.ChoiceField(
            choices=MENU_CHOICES, required=False, label='menuLocation'
            )
    highlight = forms.ChoiceField(
            choices=HIGHLIGHT_CHOICES,
            required=False,
            label='highlight'
            )
    excerpt = forms.Field(
            widget=CKEditorWidget(config_name='sv'), required=False)
    body = forms.Field(
            widget=CKEditorWidget(config_name='sv'), required=False)
    footer = forms.Field(
            widget=CKEditorWidget(config_name='sv'), required=False)


class PageForm(BaseForm):
    pass


