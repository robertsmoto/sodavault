# import itertools
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView
from django_editorjs_fields.utils import storage
from django_editorjs_fields.views import ImageUploadView
from homeapp.mixins.metadata import MetaData
from homeapp.models import APICredentials
from nanoid import generate
from svapi_py import processors
from svapi_py.api import SvApi
from typing import List, Tuple
import json
import os

from .constants import GENALPHA, DEFAULT_COLLECTIONS
from .handlers.index import POST_HANDLERS_INDEX, DELETE_HANDLERS_INDEX
from .handlers.context import CONTEXT_HANDLER_BY_PREFIX
from .handlers.partial import PARTIAL_HANDLERS_BY_DOCTYPE
from .forms import (
    GET_FORMS_BY_PREFIX, POST_FORMS_BY_PREFIX, PARTIAL_FORMS_BY_DOCTYPE
)

from django_editorjs_fields.config import (
    IMAGE_NAME,
    IMAGE_NAME_ORIGINAL,
    IMAGE_UPLOAD_PATH_DATE)

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


def add_collections(request):
    """ Adds collections to a redis sorted set named <acctID:collections>"""
    svapi = SvApi(request)
    for dt in DEFAULT_COLLECTIONS:
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


# these docTypes includes these (form) prefixes

PREFIX_INDEX = {
    'article': [
        'document',
        'article',
        'article_collection',
        'author_collection',
        'file_collection',
        'image_collection',
        'ingredient_collection',
        'recipe',
        'recipe_collection',
        'nutrition',
        'website_collection',
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


def get_initial_data(svapi, prefix, docType, docID) -> dict:
    document_initial = {
        prefix: {
            'ID': generate(GENALPHA, 16),
            'type': docType}}
    result = {}
    if docID != 'create':
        params = {'docID': docID}
        result, _ = svapi.getOne('document', params=params)
    if result:
        document_initial = result
    return document_initial


def post_handler(
        request,
        svapi=None,
        prefixes=[],
        docType='',
        docID='',
        *args,
        **kwargs):

    document_initial = get_initial_data(svapi, 'document', docType, docID)
    data = {}

    for prefix in prefixes:

        print("## prefix", prefix)
        form = POST_FORMS_BY_PREFIX.get(prefix, None)

        if not form:
            raise Exception(
                f"ManageDocument requires a form. prefix:{prefix}")

        handler = POST_HANDLERS_INDEX.get(prefix, None)

        if not handler:
            raise Exception(
                f"ManageDocument requires a handler. prefix:{prefix}")

        handler = handler(
            request=request,
            form=form,
            prefix=prefix,
            document_initial=document_initial,
            svapi=svapi,
            docType=docType,
            docID=docID
        )
        handler.handle()

        if 'collection' in prefix:
            if 'collections' not in data:
                data['collections'] = {}
            data['collections'].update(handler.cleaned_data)
        else:
            data[prefix] = handler.cleaned_data

    response = svapi.add('document', data=data)
    if response.status_code != 200:
        print("ERROR ManageDocument.post", response.status_code)


def manage_document(request, docType, docID, *args, **kwargs):

    svapi = SvApi(request)
    prefixes = PREFIX_INDEX.get(docType, [])

    # POST
    if request.method == "POST":
        print("## request.POST", request.POST)
        post_handler(
            request,
            svapi=svapi,
            prefixes=prefixes,
            docType=docType,
            docID=docID)

    # GET
    title = f'edit {docType}'
    if docID == 'create':
        title = f'create {docType}'
    breadcrumbs = [
        {'name': 'dashboard',
         'namespace': 'dashboard', 'args': ''},
        {'name': f'{docType} list',
         'namespace': 'document_list', 'args': docType},
        {'name': title.lower(),
         'namespace': '', '': ''}
    ]
    context = {
        'docType': docType,
        'docID': docID,
        'title': title
    }
    form_context = {}

    document_initial = get_initial_data(svapi, 'document', docType, docID)

    template = 'cmsapp/edit_base.html'  # default template
    UNIQUE_TEMPLATES = [
        'article',
        'author',
        'website'
    ]

    if docType in UNIQUE_TEMPLATES:
        template = f'cmsapp/edit_{docType}.html'

    for prefix in prefixes:

        # handle forms
        form = GET_FORMS_BY_PREFIX.get(prefix, None)

        initial = document_initial.get(prefix, {})
        if 'collection' in prefix:
            initial = document_initial.get('collections', {})

        if form:
            form = form(
                initial=initial,
                prefix=prefix,
                svapi=svapi,
                docType=docType,
                docID=docID
            )

            form_context[f'form_{prefix}'] = form
            continue

        # handle context only
        # 'image_collection' 'file_collection'
        handler = CONTEXT_HANDLER_BY_PREFIX.get(prefix, None)
        if handler:
            handler = handler(
                initial_data=initial,
                prefix=prefix,
                svapi=svapi,
            )
            handler.handle()
            if not handler.data:
                continue
            context[prefix] = handler.data

    return render(request, template, {
        **context,
        **form_context,
        'breadcrumbs': breadcrumbs,
    })


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

        if document_form.is_valid() and author_form.is_valid():
            data = {}
            data['document'] = document_form.cleaned_data
            data['data'] = author_form.cleaned_data
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
        self.prefix = kwargs.get('prefix', '')
        self.form = None
        init_dict = {}
        for k, v in request.GET.items():
            init_dict[f"{self.prefix}-{k}"] = v
        self.initial = init_dict
        return super().setup(request, *args, **kwargs)

    def get_template_names(self):
        prefix = self.prefix
        return [f"cmsapp/partials/form_{prefix}.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.form:
            context[f'form_{self.prefix}'] = self.form(
                self.initial or None,
                prefix=self.prefix,
                svapi=None,
                docType=self.prefix,
                docID='')

        context['docID'] = self.request.GET.get('docID', '')
        context['thumbUrl'] = self.request.GET.get('thumbUrl', '')
        context['action'] = self.request.GET.get('action', '')
        return context

    def render_to_response(self, context, **response_kwargs):
        """
        Return a response, using the `response_class` for this view, with a
        template rendered with the given context.
        Pass response_kwargs to the constructor of the response class.
        """
        response_kwargs.setdefault("content_type", self.content_type)

        print("## response kwargs", response_kwargs)
        response = self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=self.get_context_data(),
            using=self.template_engine,
            **response_kwargs)
        return response


def htmx_manage_partial(request, masterID, docID, docType, *args, **kwargs):
    svapi = SvApi(request)
    initial_data = get_initial_data(svapi, 'document', docType, docID)
    # docID = initial_data.get('document', {}).get('ID', '')
    form = None
    template = None
    context = {}

    if request.method == "DELETE":
        print("## method is DELETE")
        handler = DELETE_HANDLERS_INDEX.get(docType, None)
        if not handler:
            raise Exception("htmx_manage_partial.delete requires a handler")
        handler = handler(
            request=request,
            svapi=svapi,
            docID=docID
        )
        handler.handle()
        template = "cmsapp/partials/form_delete.html"
        return render(request, template)

    if request.method == "POST":
        """Validates 'document' fields, handles the partial form, adds data
        to the svapi repo and returns collection data to the master form."""

        data = {}
        # validates and hydrates 'document' data
        handler = PARTIAL_HANDLERS_BY_DOCTYPE.get(docType, None)
        if not handler:
            raise Exception(
                "ERROR htmx_manage_partial.POST requires a handler.")

        handler = handler(
            document_initial=initial_data.get('document', {}),
        )
        handler.handle()
        data['document'] = handler.cleaned_data
        if not docID or docID == 'create':
            docID = data['document'].get('ID', '')

        # handle the partial form
        form = PARTIAL_FORMS_BY_DOCTYPE.get(docType, None)
        handler = POST_HANDLERS_INDEX.get(docType, None)
        print("## form, handler", form, handler)
        handler = handler(
            request=request,
            form=form,
            prefix=docType,
            svapi=svapi,
            docID=docID,
            document_initial=initial_data.get(docType, {})
        )
        print("## here")
        handler.handle()
        print("## handler.cleaned_data", handler.cleaned_data)
        data[docType] = handler.cleaned_data
        print("## here 02", handler.cleaned_data)

        # add the document to SVrepo
        response = svapi.add('document', data=data)
        # print("## response", response)

        # add collection_form which has the ID field
        initial = {}
        initial['ID'] = docID
        form = POST_FORMS_BY_PREFIX.get(f"{docType}_collection", None)
        form = form(
            prefix=f"{docType}_collection",
            initial=initial
        )
        context[f"form_{docType}_collection"] = form

        template = f"cmsapp/partials/table_{docType}.html"
        context['obj'] = data
        context['masterID'] = masterID
        context['docID'] = docID
        context['docType'] = docType

    if request.method == "GET":

        print("## method is GET")
        """
          "prefix": "image", "masterID": "{{docID}}", "action": "create"
        """
        context['masterID'] = masterID
        context['docID'] = docID
        context['docType'] = docType
        # context['action'] = request.GET.get('action', '')

        form = GET_FORMS_BY_PREFIX.get(docType, None)

        if not form:
            raise Exception(
                f"ManageDocument requires a form. prefix:{docType}")

        template = f"cmsapp/partials/form_{docType}.html"
        context[f'form_{docType}'] = form(prefix=docType, initial=initial_data)

    return render(request, template, {**context})
