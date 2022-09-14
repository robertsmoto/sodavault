from django.urls import resolve
from django.utils import timezone
from django.views.generic.base import ContextMixin
import datetime
import re
import os

NOW = timezone.now()

topics = os.getenv('MD_TOPIC', '').split(',')
META_TOPIC = ", ".join(x for x in topics)

kwds = os.getenv('MD_KEYWORDS', '').split(',')
META_KEYWORDS = ", ".join(x for x in kwds)


class MetaConstructor:
    """Builds the Metadata."""

    def __init__(self, request, context):

        self.author = os.getenv('MD_AUTHOR', '')
        self.description = os.getenv('MD_DESCRIPTION', '')
        self.image = os.getenv('SOCIAL_IMAGE_SQ', '')
        self.image016 = os.getenv('MD_IMAGE016', '')
        self.image032 = os.getenv('MD_IMAGE032', '')
        self.image048 = os.getenv('MD_IMAGE048', '')
        self.image192 = os.getenv('MD_IMAGE192', '')
        self.image512 = os.getenv('MD_IMAGE512', '')
        self.keywords = META_KEYWORDS
        self.og_title = os.getenv('MD_TITLE', '')
        self.og_description = os.getenv('MD_DESCRIPTION', '')
        self.og_image = os.getenv('SOCIAL_IMAGE_SQ', '')
        self.og_locale = os.getenv('SOCIAL_LOCALE', '')
        self.og_sitename = os.getenv('MD_SITENAME', '')
        self.og_type = os.getenv('SOCIAL_TYPE', '')
        self.og_url = os.getenv('SOCIAL_URL', '')
        self.published = (
            NOW - datetime.timedelta(days=3)).strftime("%Y-%m-%d")
        self.revised = (
            NOW - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        self.sitename = os.getenv('MD_SITENAME', '')
        self.subject = os.getenv('MD_SUBJECT', '')
        self.title = os.getenv('MD_TITLE', '')
        self.topic = META_TOPIC
        self.tw_title = os.getenv('MD_TITLE', '')
        self.tw_description = os.getenv('MD_DESCRIPTION', '')
        self.tw_image = os.getenv('SOCIAL_IMAGE_SQ', '')
        self.tw_card = os.getenv('SOCIAL_TWITTER_CARD', '')
        self.tw_creator = os.getenv('SOCIAL_CREATOR', '')
        self.tw_site = os.getenv('MD_SITENAME', '')
        self.type = "article"

        # Add author data to meta_obj
        self.author = context.get('author', '')
        if self.author:
            self.author_profile = self.author.get('profile', '')
            self.author_penname = self.profile.get('penName', '')

        """If some items like robots and canonical  should be unique
        per url then they should be put on the url extra_context
        rather than in the model or view."""
        # check for robots
        self.robots = "index, follow"
        robots_value = context.get('robots', '')
        if robots_value == "no":
            self.robots = "noindex, nofollow"

        # Values from request
        self.url = request.build_absolute_uri
        canonical = context.get('canonical')
        if canonical:
            meta_canonical = request.build_absolute_uri
            if isinstance(meta_canonical, str):
                meta_canonical = re.sub(r'([?].+)', '', meta_canonical)
            self.canonical = meta_canonical

        self.url_name = resolve(request.path_info).url_name


def clean_tags(val: str, **kwargs) -> str:
    """Checks value and returns modifed value if needed."""

    if isinstance(val, datetime.date):
        val = val.strftime("%Y-%m-%d")
    if isinstance(val, str):
        val = re.sub('<[^<]+?>', '', val)

    return val


class MetaData(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # instantiate the MetaConstructor
        meta_constructor = MetaConstructor(
                request=self.request,
                context=context
                )

        """self.mdata is defined on the models and put into the view
        via dispatch()"""

        data_obj = {}
        if hasattr(self, 'mdata'):
            # print("mdata", self.mdata)
            data_obj = self.mdata

        # add/update the meta_contructor class with data_obj values
        for k, v in data_obj.items():
            vars(meta_constructor)[k] = v

        # clean the values
        for k, v in vars(meta_constructor).items():
            vars(meta_constructor)[k] = clean_tags(v)

        sitename = os.getenv('MD_SITENAME', '')
        site = f"» {sitename}"
        meta_constructor.title = f"{meta_constructor.title} {site}"

        context['metadata'] = vars(meta_constructor)

        return context
