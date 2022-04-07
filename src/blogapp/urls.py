"""iskuvault URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from blogapp import views


urlpatterns = [
    path(
        'content/',
        views.EmptyView.as_view(),
        name="blogapp-article-list",
    ),

    # path(
        # 'articles/',
        # views.ArticleListView.as_view(),
        # name="blogapp-article-list",
    # ),
    # path(
        # 'article/<slug:slug>/',
        # views.ArticleDetailView.as_view(),
        # name='blogapp-article-detail'
    # ),
    # path(
        # 'docs/',
        # views.DocListView.as_view(),
        # name="blogapp-doc-list",
    # ),
    # path(
        # 'doc/<slug:slug>/',
        # views.DocDetailView.as_view(),
        # name='blogapp-doc-detail'
    # ),
    # path(
        # 'pages/',
        # views.PageListView.as_view(),
        # name="blogapp-page-list",
    # ),
    # path(
        # 'page/<slug:slug>/',
        # views.PageDetailView.as_view(),
        # name='blogapp-page-detail'
    # ),
    # path(
        # "category/<int:category_id>/<category_name>/",
        # views.CategoryListView.as_view(),
        # name="blogapp-category-list",
    # ),
    # path(
        # "tag/<int:tag_id>/<tag_name>/",
        # views.TagListView.as_view(),
        # name="blogapp-tag-list",
    # ),
    # path(
        # "search/",
        # views.DocSearchListView.as_view(),
        # name="blogapp-search",
    # ),
]
