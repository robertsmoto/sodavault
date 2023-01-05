from django import forms
from django.core import validators
from crispy_forms.bootstrap import Div
from crispy_forms.layout import Field

DIV01 = Div(
    Field('docType', wrapper_class='col-md-2'),
    Field('ID', wrapper_class='col-md-2'),
    Field('parentID', wrapper_class='col-md-2'),
    Field('createdAt', wrapper_class='col-md-3'),
    Field('updatedAt', wrapper_class='col-md-3'),
    css_class='row mt-2',
)
DIV02 = Div(
    Field('lexi', wrapper_class='col-md-4'),
    Field('indx', wrapper_class='col-md-8'),
    css_class='row mt-2'
)


class BaseFieldsForm(forms.Form):

    docType = forms.CharField(
        disabled=True, label='DocType')
    ID = forms.CharField(disabled=True, label='ID')
    parentID = forms.ChoiceField(
        required=False,
        label='Parent',
        choices=[],
    )
    createdAt = forms.DateTimeField(
        disabled=True,
        required=False,
        label='CreatedAt',
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'}
        )
    )
    updatedAt = forms.DateTimeField(
        required=False,
        label='UpdatedAt',
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'}
        )
    )
    lexi = forms.CharField(
            label='Lexi', 
            help_text='Sortable lexiographic field, max chars = 50')
    indx = forms.CharField(
        required=False,
        label='Indx',
        help_text='Searchable text field, max words = 10, or chars = 100'
    )
