# from . import base
from cmsapp import constants as CONST
from crispy_forms.bootstrap import Accordion, AccordionGroup
from crispy_forms.bootstrap import Div, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Field, Submit, Button
from django import forms
from django.core import validators
from django.urls import reverse


class Create():
    name = forms.CharField(label='Name')
    description = forms.CharField(required=False, label='Description')

    def __init__(self, parent_choices: list, form_id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parentID'].choices = parent_choices
        self.helper = FormHelper()
        self.helper.form_id = form_id
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Accordion(
                AccordionGroup(
                    'Main',
                    Div(
                        Field('name', wrapper_class='col-md-4'),
                        Field('description', wrapper_class='col-md-8'),
                        css_class='row mt-2',
                    ),
                ),
                # AccordionGroup(
                # 'Document',
                # base.DIV01,
                # base.DIV02,
                # ),
            ),
            FormActions(
                Submit('save', 'Save changes'),
                Button(
                    'cancel', 'Cancel',
                    onclick="window.location.href = '{}';"
                            .format(reverse(
                                'collection_list',
                                kwargs={
                                    'doc_type': CONST.ARTICLECATEGORY}))),
                css_class='mt-3'
            ),
        )
