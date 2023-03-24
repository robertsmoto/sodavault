from django.views.generic.base import ContextMixin
from django.views.generic.edit import ProcessFormView
from django.shortcuts import render
from django.forms import formset_factory
from .forms import (
    ArticleForm,
    ArticleCollectionForm,
    AuthorForm,
    BookReview,
    DocumentForm,
    Endorsement,
    IngredientForm,
    LocalBusinessReview,
    NutritionForm,
    Rating,
    RecipeForm,
    WebsiteForm,
)
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django_editorjs_fields.config import (
    IMAGE_NAME,
    IMAGE_NAME_ORIGINAL,
    IMAGE_UPLOAD_PATH,
    IMAGE_UPLOAD_PATH_DATE)
from django_editorjs_fields.utils import storage
from django_editorjs_fields.views import ImageUploadView
from homeapp.mixins.metadata import MetaData
from homeapp.models import APICredentials
from svapi_py import processors
from svapi_py.api import SvApi
from typing import List, Tuple
import json
import os
from nanoid import generate

CONF = settings.CONF


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
        results, err = self.svapi.getMany('search', params={
            'docType': f"{self.docType}",
            'sortby': 'docLexi:ASC',
        })
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

    # k, *rest = k.split('_', 1)
    # if rest:
    # _nest_dict_rec(rest[0], v, out.setdefault(k, {}))
    # else:
    # out[k] = v


def flat_to_nested_dict(flat: dict) -> dict:
    result = {}
    for k, v in flat.items():
        _nest_dict_rec(k, v, result)
    return result


FORM_INDEX = {
    'article': [
        (DocumentForm, 'document'),
        (ArticleForm, 'article'),
        (RecipeForm, 'recipe'),
        (ArticleCollectionForm, 'collections')
    ],
    'articleCategory': [(DocumentForm, 'document')],
    'articleTag': [(DocumentForm, 'document')],
    'articleKeyword': [(DocumentForm, 'document')],
    'recipeCookingMethod': [(DocumentForm, 'document')],
    'recipeCuisine': [(DocumentForm, 'document')],
    'recipeCategory': [(DocumentForm, 'document')],
    'recipeSuitableForDiet': [(DocumentForm, 'document')],
    'author': [(DocumentForm, 'document'), (AuthorForm, 'author')],
    'website': [(DocumentForm, 'document'), (WebsiteForm, 'website')]
}


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
             'namespace': 'document_list', 'args': self.docType.lower()},
            {'name': self.title.lower(),
             'namespace': '', '': ''}
        ]
        self.doc_context = {
            'docType': self.docType,
            'docID': self.docID,
            'title': self.title
        }

        self.data_forms = FORM_INDEX.get(self.docType, [])
        print("## self.data_forms", self.data_forms)
        self.form_context = {}
        self.document_initial = {
            'ID': generate(size=16),
            'type': self.docType}
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        # CREATE
        if self.docID == 'create':
            for form, prefix in self.data_forms:
                self.form_context[f'form_{prefix}'] = form(
                    initial=self.document_initial
                )

        # MODIFY
        else:
            params = {'docID': self.docID}
            result, _ = self.svapi.getOne('document', params=params)
            for form, prefix in self.data_forms:
                self.form_context[f'form_{prefix}'] = form(
                    initial=result.get(prefix, {})
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
            'breadcrumbs': self.breadcrumbs,
        })

    def post(self, request, *args, **kwargs):
        data = {}

        for form, prefix in self.data_forms:
            form = form(request.POST)
            if form.is_valid():
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
        'ID': generate(size=16),
        'type': 'author'}

    if request.POST:
        print("### ######## request.POST", request.POST)
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


# def document_post(request, docType: str, *args, **kwargs):
    # DocumentFormSet = formset_factory(DocumentForm, extra=0, max_num=1)
    # AuthorFormSet = formset_factory(AuthorForm, extra=0, max_num=1)
    # # going to add via api
    # document_formset = DocumentFormSet(
    # request.POST, request.FILES, prefix='doc')
    # author_formset = AuthorFormSet(
    # request.POST, request.FILES, prefix='author')
    # if document_formset.is_valid() and author_formset.is_valid():
    # # do something with the formset.cleaned_data
    # pass

    # svapi = SvApi(request)
    # # converts from a Django QueryDict to python Dict
    # data_dict = dict(request.POST)

    # # flat data to nested dict
    # data_dict = flat_to_nested_dict(data_dict)

    # # post the data
    # response = svapi.add('document', data=data_dict)
    # if response.status_code != 200:
    # print("ERROR response status code", response.status_code)
    # return HttpResponseRedirect(
    # reverse(
    # 'document_list', args=[docType]))


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


def get_select_choices(request, *args, **kwargs) -> List[Tuple[str, str]]:
    """Endpoint for requsts to return certain select choice lists. Uses
    /search endpoint and needs docType and sortby.
    /search?docType = articleCategory & sortby = docLexi: ASC. The SvApi.makeChoices
    method needs the choiceID and choiceHuman parameters."""

    qv = request.GET.dict()  # dict of request.url query values
    # print("## qv", qv)
    select_ids = qv.get('selectedIDs', [])
    remove_id = qv.get('removeID', [])
    if request.method != 'GET':
        return []
    svapi = SvApi(request)
    params = {
        'docType': qv.get('docType', ''),
        'sortby': qv.get('sortBy', ''),
    }
    # print("## params", params)
    results, err = svapi.getMany('search', params=params)
    print("## results", results)
    print("## err", err)
    if err == 'no data':
        return JsonResponse(results, safe=False)
    raw_choices = svapi.makeChoices(
        results,
        qv.get('choiceID', ''),
        qv.get('choiceHuman', ''))
    print("## raw choices ######################", raw_choices)
    # select2 expects results in a very specific format
    # https://select2.org/data-sources/formats
    select2 = {}
    choices = []
    for i, txt in raw_choices:
        if i in remove_id:
            continue
        choice = {}
        choice['id'] = i
        choice['text'] = txt
        if i in select_ids:
            choice['selected'] = True
        choices.append(choice)

    choices.insert(0, '')
    # pagination = results.get('Pagination', {})
    pagination = {}
    pagination['more'] = pagination.get('hasNext', False)
    select2['results'] = choices
    select2['pagination'] = pagination
    return JsonResponse(select2, safe=False)


def select2_tag_post(request, *args, **kwargs):
    print("## kwargs", kwargs)
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
    print("## response", response)
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


# class FormView(FormView):

    # # form_class = DocumentForm
    # template_name = 'cmsapp/forms/attribute.html'

    # def setup(self, request, *args, **kwargs):
        # self.action = kwargs.get('action', '')
        # self.collection = kwargs.get('collection', '')
        # self.docID = kwargs.get('docID', '')
        # return super().setup(request, *args, **kwargs)

    # def get_initial(self):
        # if self.action != 'edit':
        # # provide 'new' data

        # return {
        # 'collection': self.collection,
        # 'docID': generate(size=16),
        # 'docCreatedAt': datetime.now(),
        # 'docUpdatedAt': datetime.now()
        # }

        # err = ''
        # self.svapi = SvApi(self.request)
        # initial, err = self.svapi.getOne('document', params={
        # 'docID': self.docID,
        # })
        # if err != '':
        # print("## err", err)
        # return {}
        # self.initial = initial
        # return self.initial

    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context['obj'] = self.initial
        # return context


# class DocumentEdit(FormView):

    # def setup(self, request, *args, **kwargs):
        # self.action = kwargs.get('action', '')
        # self.collection = kwargs.get('collection', '')
        # self.docID = kwargs.get('docID', '')
        # return super().setup(request, *args, **kwargs)

    # def get_form_class(self):
        # if self.collection == 'author':
        # return AuthorForm
        # if self.collection == 'website':
        # return WebsiteForm
        # return ArticleForm  # <-- default form class

    # def get_template_names(self):
        # if self.collection == 'article':
        # return 'cmsapp/edit_article.html'
        # if self.collection == 'author':
        # return 'cmsapp/edit_author.html'
        # if self.collection == 'techdoc':
        # return 'cmsapp/edit_tech_doc.html'
        # if self.collection == 'website':
        # return 'cmsapp/edit_website.html'
        # return 'cmsapp/edit_base.html'  # error to default

    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context['server'] = settings.SERVER
        # context['collection'] = self.collection
        # context['action'] = self.action
        # context['docID'] = self.docID
        # page_title = f'{self.action} {self.collection}'.title()
        # context['page_title'] = page_title
        # # documentation
        # context['docs'] = {'link': '#'}
        # # breadcrumbs
        # rev_name, rev_namespace, rev_args = breadcrum_processor(
        # self.collection)
        # context['breadcrumbs'] = [
        # {'name': 'dashboard', 'namespace': 'dashboard', 'args': ''},
        # {'name': rev_name, 'namespace': rev_namespace, 'args': rev_args},
        # {'name': page_title.lower(), 'namespace': '', 'args': ''}

        # return context
