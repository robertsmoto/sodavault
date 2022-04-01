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
    # POSTS
    path(
        '',
        views.BlogListView.as_view(
            extra_context={"doc_slug": "blogapp-blog-list"}
        ),
        name="blogapp-blog-list",
    ),
    path(
        '<post_type>/',
        views.BlogListView.as_view(
            extra_context={'doc_slug': 'blogapp-docs-list'}
        ),
        name='blogapp-docs-list'
    ),
    # should post detail include : Y/M/d ??
    path(
        '<post_type>/<slug:slug>/',
        views.BlogDetailView.as_view(
            extra_context={'doc_slug': 'blogapp-detail'}
        ),
        name='blogapp-detail'
    ),
    path(
        "category/<int:category_id>/<category_name>/",
        views.CategoryListView.as_view(
            extra_context={"doc_slug": "blogapp-category-list"}
        ),
        name="blogapp-category-list",
    ),
    path(
        "tag/<int:tag_id>/<tag_name>/",
        views.TagListView.as_view(
            extra_context={"doc_slug": "blogapp-tag-list"}
        ),
        name="blogapp-tag-list",
    ),
    path(
        "search/",
        views.DocSearchListView.as_view(
            extra_context={"doc_slug": "blogapp-search"}
        ),
        name="blogapp-search",
    ),
]
