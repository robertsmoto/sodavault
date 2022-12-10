from . import views
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [
    # using the blogapp to serve the homepage
    path(
        'article/list',
        login_required(views.ArticleList.as_view()),
        name='article-list',
       ),
]
