from . import constants as CONST
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView
from homeapp.mixins.metadata import MetaData
from homeapp.mixins.navigation import Navigation
from homeapp.models import APICredentials
from svapi_py.api import SvApi
from typing import List, Tuple
from django.http import Http404

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


class DocumentList(MetaData, Navigation, ListView):
    template_name = 'cmsapp/document_list.html'
    paginate_by = 10

    def setup(self, request, *args, **kwargs):
        self.docType = kwargs.get('doc_type', '')
        self.svapi = SvApi(request)
        results, _ = self.svapi.getMany('search', params={
            'docType': f"{self.docType}",
            'sortby': 'createdAt:DESC',
        })
        if not results[0]:
            raise Http404
        title = self.docType.replace('_', ' ').title()
        self.title = f'{title} List'
        self.object_list = results
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return self.object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"{self.docType} list".title()
        context['docType'] = self.docType
        context['breadcrumbs'] = [
            {'name': 'dashboard',
             'namespace': 'dashboard', 'args': ''},
            {'name': self.title.lower(),
             'namespace': '', '': ''}
        ]
        context['docs'] = {'link': '#'}
        return context


class DocumentNew(MetaData, Navigation, TemplateView):
    template_name = 'cmsapp/docment.html'
    success_url = '/success'
    extra_context = {
        'title': 'New Document',
        'breadcrumbs': [
            {'name': 'dashboard', 'namespace': 'dashboard'},
            {'name': 'articles', 'namespace': 'document_list'},
            {'name': 'new article', 'namespce': ''}
        ],
    }

    def setup(self, request, *args, **kwargs):
        return super().setup(request, *args, **kwargs)

    def get_form_class(self):
        """Return the form class to use."""
        if self.docType == 'doc':
            return document.DocCreate
        if self.docType == 'page':
            return document.PageCreate
        return document.ArticleCreate

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs


class DocumentEdit(MetaData, Navigation, TemplateView):
    # template_name = 'cmsapp/dashboard.html'
    template_name = 'cmsapp/forms/document_crud.html'

    def setup(self, request, *args, **kwargs):
        self.docType = kwargs.get('doc_type', '')
        self.docID = kwargs.get('doc_id', '')
        self.title = 'change this title'
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title.title()
        context['breadcrumbs'] = [
            {'name': 'dashboard',
             'namespace': 'dashboard', 'args': ''},
            {'name': self.title.lower(),
             'namespace': '', '': ''}
        ]
        context['docs'] = {'link': '#'}
        context['docType'] = self.docType
        context['docID'] = self.docID
        return context


class DocumentDelete(MetaData, Navigation, TemplateView):
    template_name = 'cmsapp/document_list.html'

    def setup(self, request, *args, **kwargs):
        self.svapi = SvApi(request)
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        results = self.svapi.getMany('set', params={
            'ID': CONST.ARTICLECATEGORY,
            'start': 0,
            'end': -1
        })
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class CollectionList(MetaData, Navigation, ListView):
    template_name = 'cmsapp/collection_list.html'
    paginate_by = 10

    def setup(self, request, *args, **kwargs):
        self.docType = kwargs.get('doc_type', '')
        self.docTypeTitle = self.docType.replace('_', ' ').title()
        self.title = f'{self.docTypeTitle} List'
        self.svapi = SvApi(request)
        results, err = self.svapi.getMany('search', params={
            'docType': self.docType,
            'sortby': 'lexi:ASC',
        })
        if err != '':
            print("## error", err)
            results = []
        forest = parent_child_list(results)
        new_list = []
        for node in forest:
            new_list = flatten_list(node, level=0, new_list=new_list)
        self.object_list = new_list
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        return self.object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['docType'] = self.docType
        context['docTypeTitle'] = self.docTypeTitle
        # lookup various attributes based on self.coll from constants module
        context['title'] = self.title
        context['breadcrumbs'] = [
            {'name': 'dashboard',
             'namespace': 'dashboard',
             'args': ''},
            {'name': self.title.lower(),
             'namespace': '',
             'args': ''},
        ]
        return context


def collection_post(request, doc_type: str):
    if request.method == 'POST':
        print("## REQEST.method is Post")
    svapi = SvApi(request)
    response = svapi.add('document', data=request.POST)
    print("## response", response)
    if response.status_code != 200:
        print("## rsponse status code", response.status_code)
    return HttpResponseRedirect(
        reverse(
            'collection_list', args=[doc_type]))


# # this one will change to function / modal
# class CollectionEdit(MetaData, Navigation, FormView):
    # template_name = 'cmsapp/crud.html'
    # form_class = collection.Create

    # def setup(self, request, *args, **kwargs):
    # self.docID = kwargs.get('doc_id', '')
    # self.idx = request.path.replace('/', '-').replace(
    # f'-{self.docID}', '').strip('-').lower()
    # self.svapi = SvApi(request)
    # obj, err = self.svapi.getOne('document', params={'ID': self.docID})
    # obj['updatedAt'] = datetime.now()
    # if err != '':
    # obj = {}
    # self.obj = obj
    # self.docType = obj.get('docType', '')
    # self.title = obj.get('name', '')
    # return super().setup(request, *args, **kwargs)

    # def get_initial(self):
    # return self.obj

    # def get_form_kwargs(self):
    # kwargs = super().get_form_kwargs()
    # kwargs['form_id'] = 'editCollection'
    # parent_q, _ = self.svapi.getMany(
    # 'search',
    # params={
    # 'docType': self.docType,
    # 'sortby': 'lexi:ASC'},
    # )
    # print("## parent_q", parent_q)
    # kwargs['parent_choices'] = self.svapi.makeChoices(
    # parent_q, 'ID', 'name')
    # print("## parent_choices", kwargs['parent_choices'])
    # return kwargs

    # def get_context_data(self, **kwargs):
    # context = super().get_context_data(**kwargs)
    # context['docType'] = self.docType
    # context['urlArgs'] = self.docID
    # context['title'] = f"Edit {self.title}"
    # context['breadcrumbs'] = [
    # {'name': 'dashboard',
    # 'namespace': 'dashboard',
    # 'args': ''},
    # {'name': 'article categories',
    # 'namespace': 'collection_list',
    # 'args': f'{self.docType}'},
    # {'name': f'edit {self.title}',
    # 'namespace': '',
    # 'args': ''}
    # ]
    # return context

    # def form_valid(self, form):
    # print("## form.cleaned -- ", form.cleaned_data)
    # response = self.svapi.modify('document', data=form.cleaned_data)
    # print(
    # "## SvApi response", response.text,
    # response.status_code,
    # response.reason)
    # return HttpResponseRedirect(self.get_success_url())

    # def get_success_url(self):
    # print("## get success url")
    # return reverse(
    # 'collection_list', kwargs={
    # 'doc_type': CONST.ARTICLECATEGORY})


def collection_delete(request, doc_type: str, doc_id: str):
    if request.method == 'POST':
        print("## REQEST.method is Post")
    svapi = SvApi(request)
    params = {
        'ID': doc_id,
    }
    print("## params", params)
    response = svapi.delete('document', params=params)
    print("## response", response)
    if response.status_code != 200:
        print("## rsponse status code", response.status_code)
    return HttpResponseRedirect(
        reverse(
            'collection_list', args=[doc_type]))


def get_document(request, *args, **kwargs) -> str:
    """Endpoint for requsts to return a json representation of a document. Uses
    the document endpoint as: /document?ID=<the_document_id>."""

    qv = request.GET.dict()  # dict of request.url query values
    print("## qv", qv)

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

    print("### im here")
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
        result_list,
        qv.get('choiceID', ''),
        qv.get('choiceHuman', ''))
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
    print("## response", response)
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
    print("## params", params)
    response = svapi.delete('set', params=params)
    print("## response", response)
    if response.status_code != 200:
        print("## rsponse status code", response.status_code)
    return HttpResponseRedirect(
        reverse(
            'set_list', args=[set_name]))
