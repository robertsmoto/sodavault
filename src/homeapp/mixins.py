from blogapp.models import Post
# from datetime import timedelta, datetime
# from decouple import config
# from django.conf import settings
from django.db.models import Q
from django.views.generic.base import ContextMixin
import pickle


class Navigation(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(Navigation, self).get_context_data(**kwargs)
        context["navigation"] = {}
        navigation = context["navigation"]
        # navigation["topics"] = Catgory.objects.all()
        """
            >>> qs = Blog.objects.values_list('id', 'name')
            >>> qs
            <QuerySet [(1, 'Beatles Blog')]>
            >>> reloaded_qs = Blog.objects.all()
            >>> reloaded_qs.query = pickle.loads(pickle.dumps(qs.query))
            >>> reloaded_qs
            <QuerySet [{'id': 1, 'name': 'Beatles Blog'}]>
        """
        # only need values for navigation
        # 'blogapp-post-detail' needs <post_type> and <slug>
        # pages_val = Post.objects
        pages_q = Post.objects.filter(
            Q(status="PUBLI") & Q(post_type="PAGE") & Q(primary_menu=True)
        ).values_list('title', 'post_type', 'slug')
        pages_q.query = pickle.loads(pickle.dumps(pages_q.query))
        navigation["pages"] = pages_q
        return context


# class MetaData(ContextMixin):
    # def get_context_data(self, **kwargs):

        # context = super(MetaData, self).get_context_data(**kwargs)
        # request = self.request
        # kwargs = self.kwargs

        # meta_dict = {}
        # # current_site = get_current_site(request)
        # now = datetime.now()
        # # published = now - timedelta(hours=12, minutes=41)
        # revised = now - timedelta(hours=5, minutes=7)

        # #  DEFAULT METADATA
        # meta_title = config('ENV_MD_TITLE')
        # meta_description = config('ENV_MD_DESCRIPTION')
        # meta_author = config('ENV_MD_AUTHOR')
        # meta_keywords = config('ENV_MD_KEYWORDS')
        # meta_subject = config('ENV_MD_SUBJECT')
        # meta_topic = config('ENV_MD_TOPIC')
        # meta_image = settings.STATIC_URL + config('ENV_MD_IMAGE')
        # meta_logo = settings.STATIC_URL + config('ENV_MD_LOGO')
        # meta_published = "Feb. 1, 2009, 8:00 a.m."
        # meta_revised = revised
        # meta_type = "article"
        # # meta_sitename = request.site.name
        # meta_url = request.build_absolute_uri()
        # # meta_sd_url = "https://" + request.site.domain
        # meta_person = ""
        # meta_canonical = ""
        # meta_abstract = ""
        # meta_h1 = ""

        # #  MODIFY META BASED ON KWARGS
        # if "title" in kwargs:
            # meta_title = kwargs["title"]

        # #  MODIFY BASED ON EXTRA CONTEXT
        # if "robots" in context:
            # robots_value = context["robots"]
            # if robots_value == "no":
                # meta_robots = "noindex, nofollow"
        # else:
            # meta_robots = "index, follow"

        # #  Basic Meta
        # meta_dict["title"] = meta_title
        # meta_dict["h1"] = meta_h1
        # meta_dict["description"] = meta_description
        # meta_dict["author"] = meta_author
        # meta_dict["keywords"] = meta_keywords
        # meta_dict["subject"] = meta_subject
        # meta_dict["topic"] = meta_topic
        # meta_dict["image"] = meta_image
        # meta_dict["logo"] = meta_logo
        # meta_dict["abstract"] = meta_abstract
        # meta_dict["published"] = meta_published
        # meta_dict["revised"] = meta_revised
        # # meta_dict["robots"] = meta_robots
        # meta_dict["canonical"] = meta_canonical
        # meta_dict["person"] = meta_person

        # #  Structrued Data
        # # meta_dict["sd_url"] = meta_sd_url

        # #  FACEBOOK
        # meta_dict["og_title"] = meta_title
        # meta_dict["og_type"] = meta_type
        # meta_dict["og_url"] = meta_url
        # # meta_dict["og_sitename"] = meta_sitename
        # meta_dict["og_description"] = meta_description
        # meta_dict["og_image"] = meta_image

        # #  TWITTER
        # meta_dict["tw_card"] = "summary"
        # meta_dict["tw_site"] = "@robertsmoto"
        # meta_dict["tw_creator"] = "@author_handle"
        # meta_dict["tw_title"] = meta_title
        # meta_dict["tw_description"] = meta_description
        # meta_dict["tw_image"] = meta_image

        # context["metadata"] = meta_dict
        # return context
