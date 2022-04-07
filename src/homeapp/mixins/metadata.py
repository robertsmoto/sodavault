from decouple import config, Csv
from django.urls import resolve
from django.utils import timezone
from django.views.generic.base import ContextMixin
import datetime
import re

NOW = timezone.now()

topics = config('ENV_MD_TOPIC', cast=Csv())
META_TOPIC = ", ".join(x for x in topics)

kwds = config('ENV_MD_KEYWORDS', cast=Csv())
META_KEYWORDS = ", ".join(x for x in kwds)


class MetaConstructor:
    """Builds the Metadata."""

    def __init__(self, request, context):

        self.author = config('ENV_MD_AUTHOR', "")
        self.description = config(
                'ENV_MD_DESCRIPTION', "")
        self.image = config('SOCIAL_IMAGE_SQ')
        self.image016 = config('ENV_MD_IMAGE016')
        self.image032 = config('ENV_MD_IMAGE032')
        self.image048 = config('ENV_MD_IMAGE048')
        self.image192 = config('ENV_MD_IMAGE192')
        self.image512 = config('ENV_MD_IMAGE512')
        self.keywords = META_KEYWORDS
        self.og_title = config('ENV_MD_TITLE', "")
        self.og_description = config(
                'ENV_MD_DESCRIPTION', "")
        self.og_image = config('SOCIAL_IMAGE_SQ')
        self.og_locale = config('SOCIAL_LOCALE')
        self.og_sitename = config('ENV_MD_SITENAME')
        self.og_type = config('SOCIAL_TYPE')
        self.og_url = config('SOCIAL_URL')
        self.published = (
            NOW - datetime.timedelta(days=3)).strftime("%Y-%m-%d")
        self.revised = (
            NOW - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        self.sitename = config('ENV_MD_SITENAME')
        self.subject = config('ENV_MD_SUBJECT', "")
        self.title = config('ENV_MD_TITLE', "")
        self.topic = META_TOPIC
        self.tw_title = config('ENV_MD_TITLE', "")
        self.tw_description = config('ENV_MD_DESCRIPTION', "")
        self.tw_image = config('SOCIAL_IMAGE_SQ')
        self.tw_card = config('SOCIAL_TWITTER_CARD')
        self.tw_creator = config('SOCIAL_CREATOR')
        self.tw_site = config('ENV_MD_SITENAME')
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

        print("###self", self.__dict__)
        print("###data_obj", data_obj)

        # add/update the meta_contructor class with data_obj values
        for k, v in data_obj.items():
            vars(meta_constructor)[k] = v

        # clean the values
        for k, v in vars(meta_constructor).items():
            vars(meta_constructor)[k] = clean_tags(v)

        # customizes 'title >> sitename' for all urls except
        # exclusion_list = [
                # 'homeapp-home',
                # 'home',
                # ]

        # if meta_constructor.url_name not in exclusion_list:

        sitename = config('ENV_MD_SITENAME')
        site = f"» {sitename}"
        meta_constructor.title = f"{meta_constructor.title} {site}"

        context['metadata'] = vars(meta_constructor)

        print("###metadata")
        return context
