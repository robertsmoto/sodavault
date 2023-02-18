from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path(
        'dashboard/',
        login_required(views.DashboardView.as_view()),
        name='dashboard'
    ),
    path(
        'form/<action>/<doc_type>/<doc_id>',
        login_required(views.FormView.as_view()),
        name='cms_form'
    ),
    # based on Redis search
    path(
        'document/list/<doc_type>',
        login_required(views.DocumentList.as_view()),
        name='document_list'
    ),
    # based on Redis json
    path(
        'document/<doc_type>',
        login_required(views.document_post),
        name='document_post'
    ),
    # login not required as there will be public queries
    path(
        'document/detail/<doc_type>/<doc_id>',
        views.DocumentDetail.as_view(),
        name='document_detail'
    ),
    path(
        'document/delete/<doc_type>/<doc_id>',
        login_required(views.document_delete),
        name='document_delete'
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
        'set/add-default-doctypes',
        login_required(views.add_default_doc_types),
        name='set_add_default_doc_types'
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
