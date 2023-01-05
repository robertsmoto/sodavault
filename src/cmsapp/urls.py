from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # based on Redis json
    path(
        'dashboard/',
        login_required(views.DashboardView.as_view()),
        name='dashboard'
    ),
    path(
        'list/<doc_type>',
        login_required(views.DocumentList.as_view()),
        name='document_list'
    ),
    path(
        'new/<doc_type>',
        login_required(views.DocumentNew.as_view()),
        name='document_new'
    ),
    path(
        'edit/<doc_type>/<doc_id>',
        login_required(views.DocumentEdit.as_view()),
        name='document_edit'
    ),
    path(
        'delete/<doc_type>/<doc_id>',
        login_required(views.DocumentDelete.as_view()),
        name='document_delete'
    ),
    path(
        'collection/list/<doc_type>/',
        login_required(views.CollectionList.as_view()),
        name='collection_list'
    ),
    # based on Redis search
    path(
        'collection/post/<doc_type>',
        login_required(views.collection_post),
        name='collection_post'
    ),
    path(
        'collection/delete/<doc_type>/<doc_id>',
        login_required(views.collection_delete),
        name='collection_delete'
    ),
    # based on Redis sorted sets
    path(
        'set/list/<set_name>',
        login_required(views.SetList.as_view()),
        name='set_list'
    ),
    path(
        'get/select/choices',
        login_required(views.get_select_choices),
        name='get_select_choices'
    ),
    path(
        'get/document',
        login_required(views.get_document),
        name='get_document'
    ),
    path(
        'set-member/add/<set_name>',
        login_required(views.set_add_member),
        name='set_add_member'
    ),
    path(
        'set-member/delete/<set_name>/<member_id>',
        login_required(views.set_delete_member),
        name='set_delete_member'
    ),
]
