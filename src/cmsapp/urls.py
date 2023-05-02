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
        login_required(views.manage_document),
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
    path(
        'select2',
        login_required(views.get_select2_choices),
        name='select2_choices'
    ),
    path(
        'htmx/form/swap/<prefix>',
        login_required(views.HtmxFormSwap.as_view()),
        name='htmx-form-swap'
    ),
    path(
        'htmx/manage/partial/<masterID>/<docID>/<docType>',
        login_required(views.htmx_manage_partial),
        name='htmx-manage-partial'
    ),
    # path(
    # 'htmx/delete/partial/<docID>/<prefix>',
    # login_required(views.HtmxDeletePartial.as_view()),
    # name='htmx-delete-partial'
    # ),
    # path(
    # 'htmx-form-trigger/<prefix>',
    # login_required(views.HtmxFormTrigger.as_view()),
    # name='htmx-form-trigger'
    # ),
]
