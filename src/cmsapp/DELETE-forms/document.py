from ckeditor.widgets import CKEditorWidget
from cmsapp import constants as CONST
from crispy_forms.bootstrap import Accordion, AccordionGroup
from crispy_forms.bootstrap import Div, Tab, TabHolder, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Button, HTML
from datetime import datetime
from django import forms
from django.utils.safestring import mark_safe
from django.urls import reverse
# from . import base


class BaseDocumentForm(forms.Form):

    STATUS_CHOICES = [
        ('DRAFT', 'draft'),
        ('review', 'review'),
        ('published', 'published'),
    ]
    HIGHLIGHT_CHOICES = [
        ('', '----'),
        ('isFeatured', 'isFeatured'),
        ('isPromoted', 'isPromoted'),
        ('isSticky', 'isSticky'),
    ]
    MENU_CHOICES = [
        ('', '----'),
        ('isPrimary', 'isPrimary'),
        ('isSecondary', 'isSecondary'),
        ('isTeriary', 'isTertiary'),
    ]

    title = forms.CharField(required=False, label='Title')
    highlight = forms.ChoiceField(
        choices=HIGHLIGHT_CHOICES,
        required=False,
        label='Highlight'
    )
    author = forms.TypedMultipleChoiceField(
        choices=[],
        required=False,
        label=mark_safe(
            '<a href="#"><i class="fa-regular fa-square-plus"'
            'style="color:green"></i></a> Author'
        ),
    )
    website = forms.TypedMultipleChoiceField(
        choices=[],
        required=False,
        label=mark_safe(
            '<a href="#"><i class="fa-regular fa-square-plus"'
            'style="color:green"></i></a> Websites'
        ),
        help_text='Article will be published on these websites.'
    )
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        label='Status'
    )
    position = forms.IntegerField(required=False, label='menuPosition')
    excerpt = forms.Field(
        widget=CKEditorWidget(config_name='sv'), required=False)
    body = forms.Field(
        widget=CKEditorWidget(config_name='sv'), required=False)
    footer = forms.Field(
        widget=CKEditorWidget(config_name='sv'), required=False)


class ArticleCreate(BaseDocumentForm):
    # fields specific to Article
    article_category = forms.TypedMultipleChoiceField(
        choices=[],
        required=False,
        label=mark_safe(
            '<a href="#"><i class="fa-regular fa-square-plus" \
                    style="color:green"></i></a> Categories'),
    )
    article_tag = forms.TypedMultipleChoiceField(
        choices=[],
        required=False,
        label=mark_safe(
            '<a href="#"><i class="fa-regular fa-square-plus" \
                    style="color:green"></i></a> Tags'),
    )
    article_keyword = forms.TypedMultipleChoiceField(
        choices=[],
        required=False,
        label=mark_safe(
            '<a href="#"><i class="fa-regular fa-square-plus" \
                    style="color:green"></i></a> Keywords'),
    )

    def __init__(
            self,
            parent_choices: list, artCat_choices: list, artTag_choices: list,
            artKey_choices: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['updatedAt'].initial = datetime.now()
        self.fields['parentID'].choices = parent_choices

        self.fields['author'].choices = artCat_choices
        self.fields['author'].widget.attrs = {
            'class': 'select2',
            'style': 'width:100%;'}

        self.fields['website'].choices = artCat_choices
        self.fields['website'].widget.attrs = {
            'class': 'select2',
            'style': 'width:100%;'}

        self.fields['article_category'].choices = artCat_choices
        self.fields['article_category'].widget.attrs = {
            'class': 'select2',
            'style': 'width:100%;'}
        self.fields['article_tag'].choices = artTag_choices
        self.fields['article_tag'].widget.attrs = {
            'class': 'select2',
            'style': 'width:100%;'}
        self.fields['article_keyword'].choices = artKey_choices
        self.fields['article_keyword'].widget.attrs = {
            'class': 'select2',
            'style': 'width:100%;'}

        # Layout Helper
        self.helper = FormHelper()
        # form and bootstrap attributes can be set here
        self.helper.form_id = 'createArticle'
        self.helper.form_method = 'post'
        # layout

        self.helper.layout = Layout(
            Accordion(
                AccordionGroup(
                    'Document',
                    base.DIV01,
                    base.DIV02,
                ),
                AccordionGroup(
                    'Title and Tags ...',
                    Div(
                        Field('title', wrapper_class='col-md-8'),
                        css_class='row mt-2'
                    ),
                    Div(
                        Field('author', wrapper_class='col-md-4'),
                        Field('website', wrapper_class='col-md-4'),
                        Field('status', wrapper_class='col-md-2'),
                        Field('highlight', wrapper_class='col-md-2'),
                        css_class='row mt-2',
                    ),

                    Div(
                        Field('article_category', wrapper_class='col-md-4'),
                        Field('article_tag', wrapper_class='col-md-4'),
                        Field('article_keyword', wrapper_class='col-md-4'),
                        css_class='row mt-2',
                    ),
                ),
                AccordionGroup('Images ...',),
                AccordionGroup('Related ...'),
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
                Button(
                    'cancel', 'Cancel',
                    # css_class='btn-primary',
                    onclick="window.location.href = '{}';"\
                            .format(reverse(
                                'document_list',
                                kwargs={
                                    'doc_type': CONST.ARTICLE}))),
                HTML(
                    "{% if success %}<p class='alert-success p-3'>Article "
                    "was saved.</p>{% endif %}"),
                css_class='mt-1'
            ),
        )
