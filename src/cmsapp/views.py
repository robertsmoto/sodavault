from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView
from homeapp.mixins.metadata import MetaData
from homeapp.models import APICredentials
from svapi_py import processors
from svapi_py.api import SvApi
from typing import List, Tuple
import json

CONF = settings.CONF


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
            'setName': "doc_type",
            'setMember': x,
        }
        response = svapi.delete('set', params=params)
        if response.status_code != 200:
            print("ERROR rsponse status code", response.status_code)


def set_delete_all(request):
    """Deletes all docTypes from account sorted set, and drops index."""
    # first get all the set members
    svapi = SvApi(request)
    params = {'setName': "doc_type"}
    results, err = svapi.getMany('set', params=params)
    if not err:
        # deletes all the set members
        set_delete_members(request, results)

    response = svapi.delete('index')
    if response.status_code != 200:
        print("ERROR rsponse status code", response.status_code)

    return HttpResponseRedirect(
        reverse(
            'set_list', args=["doc_type"]))


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
        # add doc_type index
        params = {'load': 'doc_type'}
        response = svapi.add('index', params=params)
        if response.status_code != 200:
            print("ERROR rsponse status code", response.status_code)

    return HttpResponseRedirect(
        reverse(
            'set_list', args=['doc_type']))


default_doc_types = [
    'author',
    'article_category',
    'article_tag',
    'article_keyword',
    'page_category',
    'page_tag',
    'page_keyword',
    'recipe_cook',
    'recipe_category',
    'recipe_cuisine',
    'recipe_suitable',
    'tech_doc_category',
    'tech_doc_tag',
    'tech_doc_keyword',
    'website',
]


def add_default_doc_types(request):
    # load default doc_type to set
    svapi = SvApi(request)
    for dt in default_doc_types:
        params = {
            'setName': "doc_type",
            'setMember': dt,
        }
        response = svapi.add('set', params=params)
        print("## response", response)

    return HttpResponseRedirect(
        reverse(
            'set_list', args=['doc_type']))


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


class FormView(MetaData, TemplateView):
    # if you want to use Django form view such as BaseFormView, then you
    # will need to create a django form class with form fields etc.
    # by using TemplateView, then will have the flexibility of html forms

    def setup(self, request, *args, **kwargs):
        self.action = kwargs.get('action', '')
        self.doc_type = kwargs.get('doc_type', '')
        self.doc_id = kwargs.get('doc_id', '')

        self.obj = {}
        if self.action == 'edit':
            self.svapi = SvApi(request)
            result, err = self.svapi.getOne('document', params={
                'ID': self.doc_id,
            })
            self.obj = result
        return super().setup(request, *args, **kwargs)

    def get_template_names(self):
        if self.doc_type == 'article':
            return ['cmsapp/forms/article.html']
        if self.doc_type == 'author':
            return ['cmsapp/forms/author.html']
        if self.doc_type == 'tech_doc':
            return ['cmsapp/forms/tech_doc.html']
        return ['cmsapp/forms/attribute.html']  # error to default

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['server'] = settings.SERVER
        context['obj'] = self.obj
        context['doc_type'] = self.doc_type
        context['action'] = self.action
        context['doc_id'] = self.doc_id
        page_title = f'{self.action} {self.doc_type}'.title()
        context['page_title'] = page_title
        # context['aws'] = json.dumps(self.aws)  # <-- dump to json
        # documentation
        context['docs'] = {'link': '#'}
        # breadcrumbs
        rev_name, rev_namespace, rev_args = breadcrum_processor(self.doc_type)
        context['breadcrumbs'] = [
            {'name': 'dashboard', 'namespace': 'dashboard', 'args': ''},
            {'name': rev_name, 'namespace': rev_namespace, 'args': rev_args},
            {'name': page_title.lower(), 'namespace': '', 'args': ''}
        ]
        return context


class DocumentDetail(MetaData, DetailView):
    """Detail of json document."""

    def setup(self, request, *args, **kwargs):
        self.docType = kwargs.get('doc_type', '')
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
        self.docType = kwargs.get('doc_type', '')
        self.docTypeTitle = self.docType.replace('_', ' ').title()
        self.title = f'{self.docTypeTitle} List'
        self.svapi = SvApi(request)
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

    def get_template_names(self):
        uses_document = ['document']

        if self.docType in uses_document:
            return ['cmsapp/document_list.html']

        uses_attribute = [
            'article_category',
            'article_tag',
            'article_keyword',
            'author',
            'docs_category',
            'docs_tag',
            'docs_keyword',
            'page_category',
            'page_tag',
            'page_keyword',
            'website'
        ]

        if self.docType in uses_attribute:
            return ['cmsapp/attribute_list.html']

        if self.docType == 'article':
            return ['cmsapp/article_list.html']

        return ['cmsapp/base_list.html']

    def get_queryset(self):
        return self.object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doc_type'] = self.docType
        context['doc_type_title'] = self.docTypeTitle
        context['title'] = self.title
        context['breadcrumbs'] = [
            {'name': 'dashboard',
             'namespace': 'dashboard',
             'args': ''},
            {'name': self.title.lower(),
             'namespace': '',
             'args': ''}
        ]
        context['docs'] = {'link': '#'}
        return context


def _nest_dict_rec(k, v, out: dict) -> dict:
    if isinstance(v, list):
        v = json.dumps(v) if len(v) > 1 else v[0]
    k, *rest = k.split('-', 1)
    if rest:
        _nest_dict_rec(rest[0], v, out.setdefault(k, {}))
    else:
        out[k] = v


def flat_to_nested_dict(flat: dict) -> dict:
    result = {}
    for k, v in flat.items():
        _nest_dict_rec(k, v, result)
    return result


def document_post(request, doc_type: str, *args, **kwargs):
    svapi = SvApi(request)
    # converts from a Django QueryDict to python Dict
    data_dict = dict(request.POST)
    # flat data to nested dict
    data_dict = flat_to_nested_dict(data_dict)
    # post the data
    response = svapi.add('document', data=data_dict)
    if response.status_code != 200:
        print("ERROR response status code", response.status_code)
    return HttpResponseRedirect(
        reverse(
            'document_list', args=[doc_type]))


def document_delete(request, doc_type: str, doc_id: str):
    svapi = SvApi(request)
    params = {
        'ID': doc_id,
    }
    response = svapi.delete('document', params=params)
    if response.status_code != 200:
        print("ERROR response status code", response.status_code)
    return HttpResponseRedirect(
        reverse(
            'document_list', args=[doc_type]))


def get_document(request, *args, **kwargs) -> str:
    """Endpoint for requsts to return a json representation of a document. Uses
    the document endpoint as: /document?ID=<the_document_id>."""

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
    /search?docType=article_category&sortby=lexi:ASC. The SvApi.makeChoices
    method needs the choiceID and choiceHuman parameters."""

    qv = request.GET.dict()  # dict of request.url query values
    select_ids = qv.get('selectedIDs', [])
    remove_id = qv.get('removeID', [])
    if request.method != 'GET':
        return []
    svapi = SvApi(request)
    params = {
        'docType': qv.get('docType', ''),
        'sortby': qv.get('sortby', ''),
    }
    results, err = svapi.getMany('search', params=params)
    if err == 'no data':
        return JsonResponse(results, safe=False)
    if isinstance(results, list):
        results = {}
    raw_choices = svapi.makeChoices(
        results.get('Data', []),
        qv.get('choiceID', ''),
        qv.get('choiceHuman', ''))
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
    pagination = results.get('Pagination', {})
    pagination['more'] = pagination.get('hasNext', False)
    select2['results'] = choices
    select2['pagination'] = pagination
    return JsonResponse(select2, safe=False)


class SetNew(MetaData, TemplateView):
    template_name = 'xxx'
    # form_class = collection.Create

    def setup(self, request, *args, **kwargs):
        self.svapi = SvApi(request)
        return super().setup(request, *args, **kwargs)


class SetList(MetaData, ListView):
    template_name = 'cmsapp/set_list.html'
    paginate_by = 10

    def setup(self, request, *args, **kwargs):
        self.setName = kwargs.get('set_name', '')
        self.svapi = SvApi(request)
        params = {'setName': f"{self.setName}"}
        results, err = self.svapi.getMany('set', params=params)
        # if err == 'No data returned.':
        # print("ERROR", err)
        # add_default_doc_types(request)

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
