from PIL import Image
from datetime import datetime
from django.conf import settings
import boto3
import glob
import os
from urllib.parse import urlparse, urlunparse
from nanoid import generate
from cmsapp.constants import GENALPHA

CONF = settings.CONF
USE_SPACES = CONF.get('aws', {}).get('use_spaces', False)


class ImageProcessor:

    def __init__(self, *args, **kwargs):
        self.image_field = kwargs.get('image_field', None)
        self.acct_prefix = kwargs.get('acct_prefix', 0)
        self.cleaned_data = {}
        self.filename = ''
        self.imageID = kwargs.get('imageID', '')
        if not self.imageID:
            self.imageID = generate(GENALPHA, 16)
        self.format = ''
        self.temp_filepath = ''
        self.filepath = ''
        self.sizes = [
            ('lg', 1),
            ('md', 2),
            ('sm', 4),
        ]

        self.base_specs = {
            'filename': None,
            'format': None
        }
        self.specs = {
            'lg': {
                'filename': None, 'size': None, 'resized': None
            },
            'md': {
                'filename': None, 'size': None, 'resized': None
            },
            'sm': {
                'filename': None, 'size': None, 'resized': None
            },
            'thumb': {
                'filename': None, 'size': None, 'resized': None
            }
        }

    def _create_filenames(self):

        self.filename = self.image_field.name
        split_fn = self.image_field.name.split('.')

        for label, size in self.sizes:
            self.specs[label]['filename'] = f"{self.imageID}-{label}" \
                f".{split_fn[1]}"

        self.specs['thumb']['filename'] = f"{self.imageID}-thumbnail" \
            f".{split_fn[1]}"

    def _get_format(self, img: Image):
        self.format = img.format

    def _resize(self, img: Image):

        for label, size in self.sizes:
            size = (img.width // size, img.height // size)
            self.specs[label]['size'] = size
            self.specs[label]['resized'] = img.resize(size)
        # thumbnail
        self.specs['thumb']['resized'] = img.copy()
        thumb_size = (200, 200)
        self.specs['thumb']['resized'].thumbnail(thumb_size)
        thumb = self.specs['thumb']['resized']
        self.specs['thumb']['size'] = (thumb.width, thumb.height)

    def _create_dirs(self):

        self.temp_filepath = os.path.join(
            CONF.get('dirs', {}).get('temp_dir', ''),
            self.acct_prefix
        )

        if not os.path.exists(self.temp_filepath):
            os.makedirs(self.temp_filepath)

        self.filepath = os.path.join(
            settings.MEDIA_ROOT,
            self.acct_prefix,
            datetime.now().strftime('%Y'),
            datetime.now().strftime('%m')
        )

        if not os.path.exists(self.filepath):
            os.makedirs(self.filepath)

    def _save_local(self, filepath: str):
        for k in self.specs:
            self.specs[k]['resized'].save(
                os.path.join(
                    settings.MEDIA_ROOT,
                    filepath,
                    self.specs[k]['filename']),
                self.format
            )

    def _upload_to_spaces(self):

        # configure session and client
        session = boto3.session.Session()
        region = CONF.get('aws', {}).get('region_name', '')
        endpoint = CONF.get('aws', {}).get('endpoint_url', '')
        access_key = CONF.get('aws', {}).get('access_key_id', '')
        secret_key = CONF.get('aws', {}).get('secret_access_key', '')
        bucket = CONF.get('aws', {}).get('storage_bucket_name', '')

        client = session.client(
            's3',
            region_name=region,
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

        # upload file
        for key in self.specs:

            # media_url/acct_prefix/year/month/filename
            storage_key = os.path.join(
                'media',
                self.acct_prefix,
                datetime.now().strftime('%Y'),
                datetime.now().strftime('%m'),
                self.specs.get(key, {}).get('filename', '')
            )

            filepath = os.path.join(
                self.temp_filepath,
                self.specs.get(key, {}).get('filename', '')
            )

            # CacheControl='string',
            cache_control = f"max-age={60*60*24*7}"
            # ContentType='string',
            content_type = f"image/{self.format.lower()}"

            with open(filepath, 'rb') as file_contents:
                client.put_object(
                    Bucket=bucket,
                    Key=storage_key,
                    Body=file_contents,
                    ACL='public-read',
                    CacheControl=cache_control,
                    ContentType=content_type

                )

    def _delete_temp_files(self):
        filename, extenstion = self.filename.split('.')
        search = os.path.join(self.temp_filepath, f"{filename}*")
        for filename in glob.glob(search):
            os.remove(filename)

    def _save_spaces(self):
        # files to temp_dir
        self._save_local(self.temp_filepath)
        # upload to spaces
        self._upload_to_spaces()
        # delete temp files
        self._delete_temp_files()

    def _save(self):

        if USE_SPACES:
            self._save_spaces()
        else:
            self._save_local(self.filepath)

    def _create_cleaned_data(self):

        for label in self.specs:

            if label not in self.cleaned_data:
                self.cleaned_data[label] = {}

            # width, height
            width, height = self.specs.get(label, {}).get('size', (0, 0))
            self.cleaned_data[label]['width'] = width
            self.cleaned_data[label]['height'] = height

            # url
            """
            ParseResult(scheme='http', netloc='docs.python.org:80',
                        path='/3/library/urllib.parse.html', params='',
                        query='highlight=params', fragment='url-parsing')
            """
            filename = self.specs.get(label, {}).get('filename', '')

            path = os.path.join(
                CONF.get('dirs', {}).get('media_url', ''),
                self.acct_prefix,
                datetime.now().strftime('%Y'),
                datetime.now().strftime('%m'),
                filename
            )
            url = urlunparse(['https',
                              CONF.get('aws', {}).get('custom_domain', ''),
                              path,
                              None,
                              None,
                              None])

            self.cleaned_data[label]['url'] = url

    def process(self):

        self._create_dirs()

        with Image.open(self.image_field) as img:
            self._get_format(img)
            self._create_filenames()
            self._resize(img)
            self._save()
            self._create_cleaned_data()


class ImageRemover:

    def __init__(self, *args, **kwargs):
        self.initial_data = kwargs.get('initial_data', {})

    def remove(self):

        remove_keys = {}
        remove_keys['Objects'] = []
        remove_keys['Quiet'] = False
        image_keys = ['lg', 'md', 'sm', 'thumb']
        # basename = os.path.basename(
        # os.path.normpath(CONF.get('dirs', {}).get('media_url', '')))

        for key in image_keys:
            obj = {}
            url = self.initial_data.get(key, {}).get('url', '')
            if not url:
                continue
            obj['Key'] = urlparse(url).path.strip('/')
            remove_keys['Objects'].append(obj)

        if len(remove_keys['Objects']) < 1:
            return

        # configure session and client
        session = boto3.session.Session()
        region = CONF.get('aws', {}).get('region_name', '')
        endpoint = CONF.get('aws', {}).get('endpoint_url', '')
        access_key = CONF.get('aws', {}).get('access_key_id', '')
        secret_key = CONF.get('aws', {}).get('secret_access_key', '')
        bucket = CONF.get('aws', {}).get('storage_bucket_name', '')

        client = session.client(
            's3',
            region_name=region,
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

        client.delete_objects(Bucket=bucket, Delete=remove_keys)


class PostImageHandler:

    def __init__(self, request, form, **kwargs):
        self.request = request
        self.acct_prefix = self.request.user.apicredentials.prefix[-12:]
        self.form = form  # this is not instantiated
        self.form_inst = kwargs.get('form_inst', None)
        self.prefix = kwargs.get('prefix', '')
        self.svapi = kwargs.get('svapi', None)
        self.docType = kwargs.get('docType', '')
        self.docID = kwargs.get('docID', '')
        self.document_initial = kwargs.get('document_initial', {})
        self.imageID = self.docID
        self.cleaned_data = {}

    def _handle_valid_data(self):

        # ceck if image has changed
        if 'image' in self.form_inst.changed_data:
            print("## image has changed")
            # remove old image(s) from CDN
            image_remover = ImageRemover(
                acct_prefix=self.acct_prefix,
                initial_data=self.form_inst.initial)
            image_remover.remove()
            # resize and save new image(s)
            image_field = self.form_inst.cleaned_data.get('image', None)
            img_processor = ImageProcessor(
                imageID=self.imageID,
                image_field=image_field,
                acct_prefix=self.acct_prefix,
            )
            img_processor.process()
            self.cleaned_data = img_processor.cleaned_data
            self.cleaned_data['ID'] = img_processor.imageID
            self.cleaned_data['format'] = img_processor.format
        else:
            # image has not changed --> save new information, retain old url
            self.cleaned_data = self.form_inst.initial

        self.cleaned_data['title'] = self.form_inst.cleaned_data.get(
            'title', '')
        self.cleaned_data['alt'] = self.form_inst.cleaned_data.get('alt', '')
        self.cleaned_data['caption'] = self.form_inst.cleaned_data.get(
            'caption', '')
        print("## self.cleaned_data", self.cleaned_data)

    def _handle_error(self):
        # check for file and delete it if necessary
        ...

    def handle(self):

        print("## image handler.handle()")
        print("## self.document_initial", self.document_initial)
        self.form_inst = self.form(
            self.request.POST,
            self.request.FILES,
            initial=self.document_initial.get(self.prefix, {}),
            prefix=self.prefix,
            svapi=self.svapi,
            docType=self.docType,
            docID=self.docID,
        )
        print("here handler")

        # print("## form initial", self.form_inst.initial)
        valid = self.form_inst.is_valid()
        changed = self.form_inst.has_changed()

        print("## valid, changed", valid, changed)
        if not valid:
            self._handle_error()

        elif changed:
            self._handle_valid_data()

        else:
            self.cleaned_data = self.form_inst.initial


class DeleteImageHandler:

    def __init__(self, request, **kwargs):
        self.request = request
        self.acct_prefix = self.request.user.apicredentials.prefix[-12:]
        self.svapi = kwargs.get('svapi', None)
        self.docID = kwargs.get('docID', '')

    def handle(self):
        # get document from svapi
        params = {
            'docID': self.docID
        }
        document, err = self.svapi.getOne('document', params)
        print("## DELETE document", document)
        # delete from CDN
        initial = document.get('image', {})
        image_remover = ImageRemover(initial_data=initial)
        image_remover.remove()
        # delete doc from svRepo
        print("## delete params", params)
        response = self.svapi.delete('document', params=params)
        if response.status_code != 200:
            print("ERROR response status code", response.status_code)
