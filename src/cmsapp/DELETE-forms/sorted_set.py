from crispy_forms.bootstrap import Modal, Div, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Button
from django import forms
from django.urls import reverse
from django.core.validators import RegexValidator

alphanumeric_validator = RegexValidator(r'^[a-zA-Z0-9_]*$')


class Add(forms.Form):
    set_member = forms.CharField(
        required=True,
        label='Set Member',
        help_text='Only alphanumeric characters and underscore ("_") '
        'are allowed.',
        validators=[alphanumeric_validator],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Layout Helper
        self.helper = FormHelper()
        # form and bootstrap attributes can be set here
        self.helper.form_id = 'sortedSetAdd'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Modal(
                Div(
                    Field('set_member', wrapper_class='col-md-4'),
                    css_class='row mt-2'
                ),
                FormActions(
                    Submit(
                        'submit', 'Submit',
                    ),
                    Button(
                        'cancel', 'Cancel',
                        onclick="window.location.href = '{}';"
                        .format(reverse(
                                'set_list',
                                kwargs={
                                    'set_name': 'doc_type'}))),
                    css_class='mt-1'
                ),
                css_id="setAddModal",
                title="This is my modal",
                title_class="w-100 text-center",
            )
        )


class Delete(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Layout Helper
        self.helper = FormHelper()
        # form and bootstrap attributes can be set here
        self.helper.form_id = 'sortedSetDelete'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            FormActions(
                Submit(
                    'delete', 'Delete',
                    css_class='btn-danger',
                ),
                Button(
                    'cancel', 'Cancel',
                    onclick="window.location.href = '{}';"
                            .format(reverse(
                                'set_list',
                                kwargs={
                                    'set_name': 'doc_type'}))),
                css_class='mt-1'
            ),
        )
