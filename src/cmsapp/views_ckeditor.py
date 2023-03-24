from ckeditor_uploader import views as ckviews
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from ckeditor_uploader.backends import get_backend
from django.utils.html import escape
from ckeditor_uploader.utils import storage
from django.http import HttpResponse, JsonResponse
from ckeditor_uploader import utils
import os


def custom_filepath(upload_name, request):
    print("## in custom filepath")
    print("## upload_name", upload_name)
    print("## request", request)
    cred = request.user.apicredentials
    print("## cred", cred)
    print("## cred.aid", cred.aid)
    print("## cred.pref", cred.prefix)
    return 'newpath'


class CustomUploadView(ckviews.ImageUploadView):

    def post(self, request, **kwargs):
        """
        Uploads a file and send back its URL to CKEditor.
        """
        uploaded_file = request.FILES["upload"]

        backend = get_backend()

        ck_func_num = request.GET.get("CKEditorFuncNum")
        if ck_func_num:
            ck_func_num = escape(ck_func_num)

        filewrapper = backend(storage, uploaded_file)
        allow_nonimages = getattr(
            settings, "CKEDITOR_ALLOW_NONIMAGE_FILES", True)
        # Throws an error when an non-image file are uploaded.
        if not filewrapper.is_image and not allow_nonimages:
            return HttpResponse(
                """
                <script type='text/javascript'>
                window.parent.CKEDITOR.tools.callFunction({},
                '', 'Invalid file type.');
                </script>""".format(
                    ck_func_num
                )
            )

        # this is what I've modified to change the upload path
        filepath = custom_filepath(uploaded_file.name, request)
        saved_path = filewrapper.save_as(filepath)
        url = utils.get_media_url(saved_path)

        print("## filepath", filepath)
        print("## saved_path", saved_path)
        print("## url", url)

        if ck_func_num:
            # Respond with Javascript sending ckeditor upload url.
            return HttpResponse(
                """
            <script type='text/javascript'>
                window.parent.CKEDITOR.tools.callFunction({}, '{}');
            </script>""".format(
                    ck_func_num, url
                )
            )
        else:
            _, filename = os.path.split(saved_path)
            retdata = {"url": url, "uploaded": "1", "fileName": filename}
            return JsonResponse(retdata)


upload = csrf_exempt(CustomUploadView.as_view())
