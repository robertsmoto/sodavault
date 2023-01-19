from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import TemplateView, ListView
from homeapp.mixins.metadata import MetaData
from homeapp.mixins.navigation import Navigation
from homeapp.models import APICredentials
from svapi_py.api import SvApi
from typing import List, Tuple
from django.http import Http404
import json

CONF = settings.CONF


class DashboardView(MetaData, Navigation, TemplateView):
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


def parent_child_list(data: list) -> list:
    # step 1: create all the nodes dictionary
    nodes = {}
    for i in data:
        nodes[i.get('ID', '')] = i
    # step 2: create trees and parent-child relations
    forest = []
    for i in data:
        node = nodes[i.get('ID', '')]
        pid = i.get('parentID', '')
        # either make the node a new tree or link it to its parent
        if not pid:
            # start a new tree in the forest
            forest.append(node)
        else:
            # add new_node as child to parent
            parent = nodes[pid]
            if 'children' not in parent:
                # ensure parent has a 'children' field
                parent['children'] = []
            children = parent['children']
            children.append(node)
    return forest


# flatten the tree and provide an indt field with the level
def flatten_list(node, level=0, new_list=[]) -> dict:
    node['indent'] = level * '&mdash;'
    new_list.append(node)
    if node.get('children', False):
        for child in node['children']:
            flatten_list(child, level=level + 1, new_list=new_list)
        node.pop('children', None)
    return new_list


# if you want to use Django form view such as BaseFormView, then you
# will need to create a django form class with form fields etc.
# by using TemplateView, then will have the flexibility of html forms
class ArticleFormView(MetaData, Navigation, TemplateView):
    template_name = 'cmsapp/forms/article.html'

    def setup(self, request, *args, **kwargs):
        self.doc_type = kwargs.get('doc_type', '')
        self.doc_id = kwargs.get('doc_id', '')
        self.action = "new"
        self.page_title = "New Article"
        self.obj = {}
        if "edit" in request.path:
            self.action = "edit"
            self.svapi = SvApi(request)
            result, err = self.svapi.getOne('document', params={
                'ID': self.doc_id,
            })
            self.obj = result
            title = result.get('title', '')
            self.page_title = f"Edit {title}"
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj'] = self.obj
        context['page_title'] = self.page_title.title()
        context['docs'] = {'link': '#'}
        context['doc_type'] = self.doc_type
        context['doc_id'] = self.doc_id
        context['action'] = self.action
        context['breadcrumbs'] = [
            {'name': 'dashboard',
             'namespace': 'dashboard', 'args': ''},
            {'name': 'article list',
             'namespace': 'document_list', 'args': 'article'},
            {'name': self.page_title.lower(),
             'namespace': '', 'args': ''}
        ]
        return context


class DocumentList(MetaData, Navigation, ListView):

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
            print("## error", err)
            results = []
        forest = parent_child_list(results.get('Data', []))
        new_list = []
        for node in forest:
            new_list = flatten_list(node, level=0, new_list=new_list)
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
            'docs_category',
            'docs_tag',
            'docs_keyword',
            'page_category',
            'page_tag',
            'page_keyword']

        if self.docType in uses_attribute:
            return ['cmsapp/attribute_list.html']

        if self.docType == 'article':
            return ['cmsapp/article_list.html']

        if self.docType == 'author':
            return ['cmsapp/author_list.html']

        if self.docType == 'website':
            return ['cmsapp/website_list.html']

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
    k, *rest = k.split('.', 1)
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
    data_dict = dict(request.POST.items())
    # flat data to nested dict
    data_dict = flat_to_nested_dict(data_dict)
    # post the data
    response = svapi.add('document', data=data_dict)
    if response.status_code != 200:
        print("## rsponse status code", response.status_code)
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
        print("## rsponse status code", response.status_code)
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

    if request.method != 'GET':
        return []
    svapi = SvApi(request)
    params = {
        'docType': qv.get('docType', ''),
        'sortby': qv.get('sortby', ''),
    }
    result_list, _ = svapi.getMany('search', params=params)
    choices = svapi.makeChoices(
        result_list.get('Data', []),
        qv.get('choiceID', ''),
        qv.get('choiceHuman', ''))
    print("## choices -->", choices)
    return JsonResponse(choices, safe=False)


class SetNew(MetaData, Navigation, TemplateView):
    template_name = 'xxx'
    # form_class = collection.Create

    def setup(self, request, *args, **kwargs):
        self.svapi = SvApi(request)
        return super().setup(request, *args, **kwargs)


class SetList(MetaData, Navigation, ListView):
    template_name = 'cmsapp/set_list.html'
    paginate_by = 10

    def setup(self, request, *args, **kwargs):
        self.setName = kwargs.get('set_name', '')
        self.svapi = SvApi(request)
        results, _ = self.svapi.getMany('set', params={
            'setName': f"{self.setName}"
        })
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


def set_add_member(request, set_name: str):
    member_id = request.POST.get('member_id', '')
    svapi = SvApi(request)
    params = {
        'setName': set_name,
        'setMember': member_id,
    }
    response = svapi.add('set', params=params)
    if response.status_code != 200:
        print("## rsponse status code", response.status_code)
    return HttpResponseRedirect(
        reverse(
            'set_list', args=[set_name]))


def set_delete_member(request, set_name: str, member_id: str):
    if request.method == 'POST':
        print("## REQEST.method is Post")
    svapi = SvApi(request)
    params = {
        'setName': set_name,
        'setMember': member_id,
    }
    response = svapi.delete('set', params=params)
    if response.status_code != 200:
        print("## rsponse status code", response.status_code)
    return HttpResponseRedirect(
        reverse(
            'set_list', args=[set_name]))
