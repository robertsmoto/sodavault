"""sodavault URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path
from django_registration.backends.one_step.views import RegistrationView
from django_editorjs_fields.views import ImageByUrl, LinkToolView
from cmsapp.views import S3ImageUploadView
import debug_toolbar


class CustomRegistrationView(RegistrationView):
    def get_context_data(self, **kwargs):
        context = super(
            CustomRegistrationView, self).get_context_data(**kwargs)
        context["context"] = context
        return context


class CustomLoginView(LoginView):
    def get_context_data(self, **kwargs):
        context = super(CustomLoginView, self).get_context_data(**kwargs)
        context["context"] = context
        return context


class CustomLogoutView(LogoutView):
    def get_context_data(self, **kwargs):
        context = super(CustomLogoutView, self).get_context_data(**kwargs)
        context["context"] = context
        return context


admin.site.index_title = 'Control Panel'
admin.site.site_title = 'SODAVault Admin'

urlpatterns = [
    path('', include('homeapp.urls')),
    path('cms/', include('cmsapp.urls')),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path(
        'accounts/login/',
        CustomLoginView.as_view(),
        name='django-registration-login'),
    path(
        'accounts/logout/',
        CustomLogoutView.as_view(),
        name='django-registration-logout'),
    path(
        'accounts/register/',
        CustomRegistrationView.as_view(success_url='/dashboard/'),
        name='django-registration-register'),
]

urlpatterns += [
    path("select2/", include("django_select2.urls")),
]

urlpatterns += [
    path(
        'image_upload/',
        login_required(S3ImageUploadView.as_view()),
        name='editorjs_image_upload',
    ),
    path(
        'image_by_url/',
        ImageByUrl.as_view(),
        name='editorjs_image_by_url',
    ),
    path(
        'linktool/',
        login_required(LinkToolView.as_view()),
        name='editorjs_linktool',
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
