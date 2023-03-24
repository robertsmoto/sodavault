from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path(
        'dashboard/',
        login_required(views.DashboardView.as_view()),
        name='dashboard'
    ),
    # based on Redis search
    path(
        'document/list/<docType>',
        login_required(views.DocumentList.as_view()),
        name='document_list'
    ),
    # edit forms
    path(
        'manage/<docType>/<docID>',
        login_required(views.ManageDocument.as_view()),
        name='manage_document'
    ),

    # login not required as there will be public queries
    path(
        'document/detail/<docType>/<docID>',
        views.DocumentDetail.as_view(),
        name='document_detail'
    ),
    path(
        'document/delete/<docType>/<docID>',
        login_required(views.document_delete),
        name='document_delete'
    ),
    path(
        'select2/tag/post',
        login_required(views.select2_tag_post),
        name='select2_tag_post'
    ),
    # indexing, action = 'reindex' or 'add'
    path(
        'index/<action>',
        login_required(views.modify_index),
        name='modify_index'
    ),
    path(
        'set/list/<set_name>',
        login_required(views.SetList.as_view()),
        name='set_list'
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
    path(
        'set/add-collections',
        login_required(views.add_collections),
        name='add_collections'
    ),
    path(
        'set/delete-all',
        login_required(views.set_delete_all),
        name='set_delete_all_members'
    ),
    # ajax request endpoints
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
]
