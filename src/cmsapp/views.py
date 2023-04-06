from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import ProcessFormView
from django_editorjs_fields.utils import storage
from django_editorjs_fields.views import ImageUploadView
from homeapp.mixins.metadata import MetaData
from homeapp.models import APICredentials
from nanoid import generate
from svapi_py import processors
from svapi_py.api import SvApi
from typing import List, Tuple
import itertools
import json
import os

from .forms import (
    ArticleForm,
    ArticleCollectionForm,
    AuthorForm,
    BookReview,
    DocumentForm,
    Endorsement,
    FileForm,
    IngredientForm,
    ImageForm,
    LocalBusinessReview,
    NutritionForm,
    Rating,
    RecipeForm,
    WebsiteForm,)

from django_editorjs_fields.config import (
    IMAGE_NAME,
    IMAGE_NAME_ORIGINAL,
    # IMAGE_UPLOAD_PATH,
    IMAGE_UPLOAD_PATH_DATE)

CONF = settings.CONF
GENALPHA = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


class S3ImageUploadView(ImageUploadView):
    """Custom image upload view to use with editor_js."""

    def post(self, request):
        """Override the superclass post method."""
        if 'image' in request.FILES:
            the_file = request.FILES['image']
            allowed_types = [
                'image/jpeg',
                'image/jpg',
                'image/pjpeg',
                'image/x-png',
                'image/png',
                'image/webp',
                'image/gif',
            ]
            if the_file.content_type not in allowed_types:
                return JsonResponse(
                    {'success': 0, 'message': 'You can only upload images.'}
                )

            filename, extension = os.path.splitext(the_file.name)

            if IMAGE_NAME_ORIGINAL is False:
                filename = IMAGE_NAME(filename=filename, file=the_file)

            filename += extension

            # custom upload path
            prefix = request.user.apicredentials.prefix[-12:]
            upload_path = f"{prefix}/"

            if IMAGE_UPLOAD_PATH_DATE:
                upload_path += datetime.now().strftime(IMAGE_UPLOAD_PATH_DATE)

            path = storage.save(
                os.path.join(upload_path, filename), the_file
            )
            link = storage.url(path)

            return JsonResponse({'success': 1, 'file': {"url": link}})
        return JsonResponse({'success': 0})


def set_add_member(request, set_name: str):
    member_id = request.POST.get('member_id', '')
    svapi = SvApi(request)
    params = {
        'setName': set_name,
        'setMember': member_id,
    }
    response = svapi.add('set', params=params)
    if response.status_code != 200:
        print("ERROR response status code", response.status_code)
    return HttpResponseRedirect(
        reverse(
            'set_list', args=[set_name]))


def set_delete_member(request, set_name: str, member_id: str):
    if request.method == 'POST':
        print("ERROR REQEST.method is Post")
    svapi = SvApi(request)
    params = {
        'setName': set_name,
        'setMember': member_id,
    }
    response = svapi.delete('set', params=params)
    if response.status_code != 200:
        print("ERROR rsponse status code", response.status_code)
    return HttpResponseRedirect(
        reverse(
            'set_list', args=[set_name]))


def set_delete_members(request, results):
    svapi = SvApi(request)
    for x in results:
        params = {
            'setName': "collections",
            'setMember': x,
        }
        response = svapi.delete('set', params=params)
        if response.status_code != 200:
            print("ERROR rsponse status code", response.status_code)


def set_delete_all(request):
    """Deletes all collections from account sorted set, and drops index."""
    # first get all the set members
    svapi = SvApi(request)
    params = {'setName': "collections"}
    results, err = svapi.getMany('set', params=params)
    if not err:
        # deletes all the set members
        set_delete_members(request, results)

    response = svapi.delete('index')
    if response.status_code != 200:
        print("ERROR rsponse status code", response.status_code)

    return HttpResponseRedirect(
        reverse(
            'set_list', args=["collections"]))


def modify_index(request, action: str):
    """Will reindex or append index. Reindex drops current index, then adds the
    base index schema. Append adds doc_types to the index.
    Use either action='reindex' or action='append'."""

    svapi = SvApi(request)
    if action == 'reindex':
        # delete account index
        params = {}
        response = svapi.delete('index', params=params)
        if response.status_code != 200:
            print("ERROR rsponse status code", response.status_code)
        # load default index
        params = {'load': 'default'}
        response = svapi.add('index', params=params)
        if response.status_code != 200:
            print("ERROR rsponse status code", response.status_code)

    if action == 'append':
        # add collections to index
        params = {'load': 'collections'}
        response = svapi.add('index', params=params)
        if response.status_code != 200:
            print("ERROR rsponse status code", response.status_code)

    return HttpResponseRedirect(
        reverse(
            'set_list', args=['collections']))


COLLECTIONS = [
    'articleCategory',
    'articleTag',
    'articleKeyword',
    'author',
    'pageCategory',
    'pageTag',
    'pageKeyword',
    'recipeCookingMethod',
    'recipeCategory',
    'recipeCuisine',
    'recipeSuitableForDiet',
    'techdocCategory',
    'techdocTag',
    'techdocKeyword',
    'website',
]


def add_collections(request):
    """ Adds collections to a redis sorted set named <acctID:collections>"""
    svapi = SvApi(request)
    for dt in COLLECTIONS:
        params = {
            'setName': "collections",
            'setMember': dt,
        }
        _ = svapi.add('set', params=params)

    return HttpResponseRedirect(
        reverse(
            'set_list', args=['collections']))


class DashboardView(MetaData, TemplateView):
    """Currently redering a simple template."""
    template_name = 'cmsapp/dashboard.html'

    def setup(self, request, *args, **kwargs):
        self.title = 'Dashboard'
        # set the session variables here
        apiCred = APICredentials.objects.get(user=request.user)
        aid = apiCred.aid
        auth = apiCred.auth
        prefix = apiCred.prefix
        request.session[request.user.id] = {
            'aid': aid,
            'auth': auth,
            'prefix': prefix,
        }
        request.session.set_expiry(60 * 60 * 20)  # <-- 24 hrs
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['breadcrumbs'] = [
            {'name': 'dashboard', 'namespce': '', 'args': ''}
        ]
        return context


def breadcrum_processor(doc_type: str) -> (str, str, str):
    rev_name = ' '.join(doc_type.split('_')) + ' list'
    rev_namespace = 'document_list'
    rev_args = doc_type
    return rev_name, rev_namespace, rev_args


class DocumentDetail(MetaData, DetailView):
    """Detail of json document."""

    def setup(self, request, *args, **kwargs):
        self.docType = kwargs.get('docType', '')
        self.docID = kwargs.get('doc_id', '')
        self.docTypeTitle = self.docType.replace('_', ' ').title()
        self.title = f'{self.docTypeTitle} List'
        # use admin headers for these requests
        headers = {
            'Aid': CONF.get('svapi', {}).get('aid', ''),
            'Auth': CONF.get('svapi', {}).get('auth', ''),
            'Prefix': CONF.get('svapi', {}).get('prefix', ''),
            'Content-Type': 'application/json'
        }
        self.svapi = SvApi(request, headers)
        results, err = self.svapi.getMany('search', params={
            'docType': f"{self.docType}",
            'sortby': 'lexi:ASC',
        })
        # error handling, decide how to do this
        if err != '':
            results = {}
        forest = processors.parent_child_list(results.get('Data', []))
        new_list = []
        for node in forest:
            new_list = processors.flatten_list(
                node, level=0, new_list=new_list)
        self.object_list = new_list
        return super().setup(request, *args, **kwargs)


class DocumentList(MetaData, ListView):

    paginate_by = 10

    def setup(self, request, *args, **kwargs):
        self.docType = kwargs.get('docType', '')
        # self.docTypeTitle = self.docType.replace('_', ' ').title()
        self.title = f'{self.docType} List'
        self.svapi = SvApi(request)
        params = {
            'qs': f"@docType:{{{self.docType}}}",
            'sortBy': 'docLexi:ASC',
        }
        results, err = self.svapi.getMany('search', params=params)
        if err != '':
            print("ERROR", err)
            results = {}
        forest = processors.parent_child_list(results)
        new_list = []
        for node in forest:
            new_list = processors.flatten_list(
                node, level=0, new_list=new_list)
        self.object_list = new_list

        return super().setup(request, *args, **kwargs)

    def get_template_names(self):

        templates = ['cmsapp/list_base.html']

        USE_UNIQUE_TEMPLATE = [
            'article',
            'author',
            'website',
        ]

        if self.docType in USE_UNIQUE_TEMPLATE:
            templates = [f'cmsapp/list_{self.docType}.html']

        return templates

    def get_queryset(self):
        return self.object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['docType'] = self.docType
        context['title'] = self.title
        context['breadcrumbs'] = [
            {'name': 'dashboard',
             'namespace': 'dashboard',
             'args': ''},
            {'name': f'{self.docType} list',
             'namespace': '',
             'args': ''}
        ]
        context['docs'] = {'link': '#'}
        return context


def _nest_dict_rec(k, v, out: dict) -> dict:
    if isinstance(v, list):
        v = json.dumps(v) if len(v) > 1 else v[0]
    out[k] = v
    return out

def flat_to_nested_dict(flat: dict) -> dict:
    result = {}
    for k, v in flat.items():
        _nest_dict_rec(k, v, result)
    return result


FORMS_BY_PREFIX = {
    'document': DocumentForm,
    'collections': ArticleCollectionForm,
    'article': ArticleForm,
    'author': AuthorForm,
    'bookReview': BookReview,
    'endorsement': Endorsement,
    'file': FileForm,
    'ingredient': IngredientForm,
    'image': ImageForm,
    'localBusiness': LocalBusinessReview,
    'nutrition': NutritionForm,
    'rating': Rating,
    'recipe': RecipeForm,
    'website': WebsiteForm
}

# the 'article' form prefix includes these [form prefixes]
PREFIX_INDEX = {
    'article': [
        'document',
        'collections',
        'article',
        'file',
        'image',
        'ingredient',
        'recipe',
        'nutrition',
    ],
    'articleCategory': ['document'],
    'articleTag': ['document'],
    'articleKeyword': ['document'],
    'recipeCookingMethod': ['document'],
    'recipeCuisine': ['document'],
    'recipeCategory': ['document'],
    'recipeSuitableForDiet': ['document'],
    'author': ['document', 'author'],
    'website': ['document', 'website']
}

# collections by docType
COLLECTIONS_INDEX = {
    'article': [
        'author',
        'articleCategory',
        'articleTag',
        'articleKeyword',
        'articleStatus',
        'articleHighlight',
        'recipeCookingMethod',
        'recipeCuisine',
        'recipeCategory',
        'recipeSuitableForDiet',
        'website',
    ],
}


# for select controls that use tags input by users
SELECT2_TAG_INDEX = {
    'article': [
        'articleCategory',
        'articleTag',
        'articleKeyword',
        'recipeCookingMethod',
        'recipeCuisine',
        'recipeCategory',
        'recipeSuitableForDiet',
    ],
}

DYNAMIC_FORMS = {
    'ingredient': ('ID', 'name', 'quantity', 'unit', 'note'),
    'image': ()
}


class Select2ErrorHandler:

    def __init__(self, request, form, **kwargs):
        self.request = request
        self.form = form
        self.prefix = kwargs.get('prefix', '')
        self.field_name = kwargs.get('f', '')
        self.svapi = kwargs.get('svapi', '')
        self.choices_index = {}
        self.post_values = []

    def _inspect_cleaned_data(self):
        """Adds field to the form.cleaned_data if it does not exist."""
        self.form.cleaned_data[self.field_name] = self.form.cleaned_data.get(
            self.field_name, [])
        return self

    def _create_chioces_index(self):
        """Creates a choices index."""
        choices = self.form.fields[self.field_name].choices
        for cid, ctext in choices:
            self.choices_index[cid] = ctext
        print("## choices index", self.choices_index)
        return self

    def _get_post_values(self):
        """Gets the exiting request.POST values for given field_name."""
        self.post_values = self.request.POST.getlist(
            f"{self.prefix}-{self.field_name}", [])
        return self

    def _add_to_SODAvault(self, tag: str):
        now = datetime.now()
        new_pid = generate(GENALPHA, 16)
        key_data = {
            'document': {
                'ID': new_pid,
                'type': self.field_name,
                'title': tag,
                'description': f"{tag.title()} autoGen",
                'lexi': f"{self.field_name[0:3]}_{self.field_name[0:3]}_"
                        f"{tag[0:3]}",
                'index': '',
                'createdAt': now,
                'updatedAt': now,
            }}

        response = self.svapi.add('document', data=key_data)
        if response.status_code != 200:
            print(f"ERROR {response}")

        print("## added to SODAvault", key_data)
        return new_pid

    def _add_to_cleaned_data(self, pid: tuple):
        self.form.cleaned_data[self.field_name].append(pid)

    def _append_field_chioces(self, data: tuple):
        self.form.fields[self.field_name].choices.append(data)

    def _process_existing_choices(self):
        """Adds existing choices back into the cleaned data."""
        for pid in self.post_values:
            ctext = self.choices_index.get(pid, '')
            if ctext:
                self._add_to_cleaned_data(pid)

    def _process_new_terms(self):
        """Adds new terms to sodaVault as document, and adds to choices."""
        for pid in self.post_values:
            ctext = self.choices_index.get(pid, '')
            if ctext:
                continue
            tag = pid
            new_pid = self._add_to_SODAvault(tag)
            self._add_to_cleaned_data(new_pid)
            self._append_field_chioces((new_pid, tag))

    def handle(self):
        """Finds and processes new Select2 Terms."""
        self._inspect_cleaned_data()
        self._create_chioces_index()
        self._get_post_values()
        self._process_existing_choices()
        self._process_new_terms()


SELECT2_INDEX = {
    'document': [
        ('parentID', 'docLexi:ASC')
    ],
    'article': [
        ('articleCategory', 'docLexi:ASC'),
        ('articleTag', 'docLexi:ASC'),
        ('articleKeyword', 'docLexi:ASC'),
        ('author', 'docLexi:ASC'),
        ('recipeCookingMethod', 'docLexi:ASC'),
        ('recipeCuisine', 'docLexi:ASC'),
        ('recipeCategory', 'docLexi:ASC'),
        ('recipeSuitableForDiet', 'docLexi:ASC'),
        ('website', 'docLexi:ASC')
    ],
}


class Select2WidgetUpdater:

    def __init__(self, request, form, **kwargs):
        self.request = request
        self.form = form
        self.svapi = kwargs.get('svapi', '')
        self.docID = kwargs.get('docID', '')
        self.docType = kwargs.get('docType', '')
        self.prefix = kwargs.get('prefix', '')
        select2_index = kwargs.get('select2_index', {})
        self.fields = select2_index.get(self.docType, [])
        if self.prefix:
            self.fields = select2_index.get(self.prefix, [])

    def _make_choices(self):
        for field, sortBy in self.fields:
            docType = field
            if self.prefix:
                docType = self.docType
            params = {'qs': f'@docType:{{{docType}}}'}
            print("## params", params)
            results, err = self.svapi.getMany('search', params=params)
            if err == 'no data':
                continue
            choices = self.svapi.makeChoices(results, self.docID)
            self.form.base_fields[field].choices = choices

    def update(self):
        self._make_choices()


class ManageDocument(ProcessFormView):

    def setup(self, request, *args, **kwargs):
        self.docType = kwargs.get('docType', '')
        self.docID = kwargs.get('docID', '')
        self.svapi = SvApi(request)
        self.title = f'edit {self.docType}'
        if self.docID == 'create':
            self.title = f'create {self.docType}'
        self.breadcrumbs = [
            {'name': 'dashboard',
             'namespace': 'dashboard', 'args': ''},
            {'name': f'{self.docType} list',
             'namespace': 'document_list', 'args': self.docType},
            {'name': self.title.lower(),
             'namespace': '', '': ''}
        ]
        self.doc_context = {
            'docType': self.docType,
            'docID': self.docID,
            'title': self.title
        }
        self.prefixes = PREFIX_INDEX.get(self.docType, [])
        self.form_context = {}
        self.formset_context = {}
        self.document_initial = {
            'document': {
                'ID': generate(GENALPHA, 16),
                'type': self.docType}}
        result = {}
        if self.docID != 'create':
            params = {'docID': self.docID}
            result, _ = self.svapi.getOne('document', params=params)
        if result:
            self.document_initial = result
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # instantiate forms
        for prefix in self.prefixes:
            form = FORMS_BY_PREFIX.get(prefix, None)
            if not form:
                continue

            if prefix == 'collections':
                select2_updater = Select2WidgetUpdater(
                    request=request,
                    form=form,
                    svapi=self.svapi,
                    docType=self.docType,
                    docID=self.docID,
                    select2_index=SELECT2_INDEX)
                select2_updater.update()
                form = select2_updater.form

            if prefix == 'document':
                select2_updater = Select2WidgetUpdater(
                    request=request,
                    form=form,
                    svapi=self.svapi,
                    prefix='document',
                    docType=self.docType,
                    docID=self.docID,
                    select2_index=SELECT2_INDEX)
                select2_updater.update()
                form = select2_updater.form

            self.form_context[f'form_{prefix}'] = form(
                initial=self.document_initial.get(prefix, {}),
                prefix=prefix
            )

        template = 'cmsapp/edit_base.html'  # default template
        UNIQUE_TEMPLATES = [
            'article',
            'author',
            'website'
        ]

        if self.docType in UNIQUE_TEMPLATES:
            template = f'cmsapp/edit_{self.docType}.html'

        return render(request, template, {
            **self.doc_context,
            **self.form_context,
            **self.formset_context,
            'breadcrumbs': self.breadcrumbs,
        })

    def post(self, request, *args, **kwargs):
        data = {}
        for prefix in self.prefixes:
            form = FORMS_BY_PREFIX.get(prefix, None)
            if not form:
                continue
            form = form(request.POST, request.FILES, prefix=prefix)
            is_valid = form.is_valid()

            if is_valid:
                dynamic_fields = DYNAMIC_FORMS.get(prefix, [])

                if not dynamic_fields:
                    data[prefix] = form.cleaned_data
                    continue

                IDs = request.POST.getlist(f"{prefix}-ID", None)
                names = request.POST.getlist(f"{prefix}-name", None)
                quantities = request.POST.getlist(
                    f"{prefix}-quantity", None)
                units = request.POST.getlist(f"{prefix}-unit", None)
                notes = request.POST.getlist(f"{prefix}-note", None)
                data[prefix] = request.POST.getlist(prefix, [])
                for a, b, c, d, e in itertools.zip_longest(
                        IDs, names, quantities, units, notes):
                    obj = {}
                    if not a:
                        a = generate(GENALPHA, 16)
                    obj['ID'] = a
                    obj['name'] = b
                    obj['quantity'] = c
                    obj['unit'] = d
                    obj['note'] = e
                    data[prefix].append(obj)

            else:
                select2_tag_list = SELECT2_TAG_INDEX.get(self.docType, [])
                for f, v in form.errors.as_data().items():
                    # ignores errors that are not select2 tags
                    if f not in select2_tag_list:
                        continue

                    error_handler = Select2ErrorHandler(
                        request=request,
                        form=form,
                        svapi=self.svapi,
                        prefix=prefix,
                        f=f
                    )
                    error_handler.handle()
                    form.cleaned_data = error_handler.form.cleaned_data

                data[prefix] = form.cleaned_data

        response = self.svapi.add('document', data=data)
        if response.status_code != 200:
            print("ERROR", response.status_code)

        return HttpResponseRedirect(
            reverse(
                'document_list', args=[self.docType]))


def manage_author(request, docID=None):

    svapi = SvApi(request)
    context = {
        'docType': 'author',
        'docID': docID
    }
    document_initial = {
        'ID': generate(GENALPHA, 16),
        'type': 'author'}

    if request.POST:
        document_form = DocumentForm(request.POST)
        author_form = AuthorForm(request.POST)

        print("## valid", document_form.is_valid(), author_form.is_valid())

        if document_form.is_valid() and author_form.is_valid():
            print("## is valid")
            data = {}
            data['document'] = document_form.cleaned_data
            data['data'] = author_form.cleaned_data
            print("## clean data", data)
            response = svapi.add('document', data=data)

            return HttpResponseRedirect(
                reverse(
                    'document_list', args=['author']))

    elif docID == 'create':
        document_form = DocumentForm(
            initial={
                **document_initial
            }
        )
        author_form = AuthorForm()

        return render(request, 'cmsapp/edit_author.html', {
            'form_author': author_form,
            'form_doc': document_form,
            **context
        })

    else:
        params = {'docID': docID}
        result, err = svapi.getOne('document', params=params)
        if err != '':
            print("ERROR", err)

        document_form = DocumentForm(initial=result.get('document', {}))
        author_form = AuthorForm(initial=result.get('data', {}))

        return render(request, 'cmsapp/edit_author.html', {
            'form_author': author_form,
            'form_doc': document_form,
            **context
        })

    return HttpResponse("something went wrong")


def document_delete(request, docType: str, docID: str):
    svapi = SvApi(request)
    params = {
        'docID': docID,
    }
    response = svapi.delete('document', params=params)
    if response.status_code != 200:
        print("ERROR response status code", response.status_code)
    return HttpResponseRedirect(
        reverse(
            'document_list', args=[docType]))


def get_document(request, *args, **kwargs) -> str:
    """Endpoint for requsts to return a json representation of a document. Uses
    the document endpoint as: / document?ID = <the_document_id > ."""

    qv = request.GET.dict()  # dict of request.url query values
    if request.method != 'GET':
        return '{}'
    svapi = SvApi(request)
    params = {
        'ID': qv.get('doc_id', ''),
    }
    document, _ = svapi.getOne('document', params=params)
    return JsonResponse(document, safe=False)


def get_select2_choices(request, *args, **kwargs) -> List[Tuple[str, str]]:
    """Endpoint for requsts to return certain select choice lists. Uses
    /search endpoint and needs docType and sortby.
    /search?docType = articleCategory & sortby = docLexi: ASC. The SvApi.makeChoices
    method needs the choiceID and choiceHuman parameters."""

    if request.method != 'GET':
        return []

    qv = request.GET.dict()  # dict of request.url query values
    term = qv.get('term', '')
    docType = qv.get('docType', '')
    sortBy = qv.get('sortBy', '')
    docID = qv.get('docID', '')
    selected_ids = qv.get('selectedIDS', [])

    svapi = SvApi(request)
    params = {
        'qs': f"@docType:{{{docType}}}@docIndex:{term}*",
        'sortBy': sortBy
    }

    results, err = svapi.getMany('search', params=params)

    if err == 'no data':
        select2 = {}
        select2['more'] = False
        select2['results'] = []
        return JsonResponse(select2, safe=False)

    raw_choices = svapi.makeChoices(results)

    select2 = {}
    choices = []
    for cid, txt in raw_choices:
        if cid == docID:
            continue
        choice = {}
        choice['id'] = cid
        choice['text'] = txt
        if cid in selected_ids:
            choice['selected'] = True
        choices.append(choice)

    # pagination = results.get('Pagination', {})
    select2 = {}
    select2['more'] = False
    select2['results'] = choices

    return JsonResponse(select2)


def select2_tag_post(request, *args, **kwargs):
    svapi = SvApi(request)
    # converts from a Django QueryDict to python Dict
    data_dict = dict(request.POST)
    data_dict = flat_to_nested_dict(data_dict)
    data = {}
    data['document'] = {}
    for k, v in data_dict.items():
        data['document'][k] = v
    # post the data
    response = svapi.add('document', data=data)
    return JsonResponse({
        "status": "success",
        "data": {"id": "thisisID", "text": "thisisTEXT"}},
        safe=False)


class SetNew(MetaData, TemplateView):
    template_name = 'xxx'
    # form_class = collection.Create

    def setup(self, request, *args, **kwargs):
        self.svapi = SvApi(request)
        return super().setup(request, *args, **kwargs)


class SetList(MetaData, ListView):
    template_name = 'cmsapp/list_set.html'
    paginate_by = 10

    def setup(self, request, *args, **kwargs):
        self.setName = kwargs.get('set_name', '')
        self.svapi = SvApi(request)
        params = {'setName': f"{self.setName}"}
        results, err = self.svapi.getMany('set', params=params)
        title = self.setName.replace('_', ' ').title()
        self.title = f'{title} List'
        self.object_list = results
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return self.object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title.title()
        context['setName'] = self.setName
        context['breadcrumbs'] = [
            {'name': 'dashboard',
             'namespace': 'dashboard', 'args': ''},
            {'name': self.title.lower(),
             'namespace': '', '': ''}
        ]
        context['docs'] = {'link': '#'}
        return context


class HtmxFormSwap(TemplateView):

    def setup(self, request, *args, **kwargs):
        print("## request", request)
        print("## request.GET", request.GET, type(request.GET))

        self.prefix = kwargs.get('prefix', '')
        self.form = FORMS_BY_PREFIX.get(self.prefix, None)
        init_dict = {}
        for k, v in request.GET.items():
            init_dict[f"{self.prefix}-{k}"] = v
        self.initial = init_dict
        return super().setup(request, *args, **kwargs)

    def get_template_names(self):
        return [f"cmsapp/partials/form_{self.prefix}.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.form:
            context[f'form_{self.prefix}'] = self.form(
                self.initial or None, prefix=self.prefix)
        return context

    def render_to_response(self, context, **response_kwargs):
        """
        Return a response, using the `response_class` for this view, with a
        template rendered with the given context.
        Pass response_kwargs to the constructor of the response class.
        """
        print("## request", self.request)
        response_kwargs.setdefault("content_type", self.content_type)

        response = self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=self.get_context_data(),
            using=self.template_engine,
            **response_kwargs)
        return response
