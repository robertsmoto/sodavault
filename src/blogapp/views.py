# from blogapp.models import Article, Doc, Page
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.db.models import Q
from homeapp.mixins.breadcrumbs import BrCrumb
from homeapp.mixins.metadata import MetaData
from homeapp.mixins.navigation import Navigation


class EmptyView(BrCrumb, MetaData, Navigation, ListView):
    pass



# class ArticleListView(BrCrumb, MetaData, Navigation, ListView):

    # template_name = "blogapp/article_list.html"
    # paginate_by = 30

    # def get_queryset(self, *args, **kwargs):
        # list_q = Article.objects.filter(
            # status="PUBLI",
            # parent__isnull=True,
            # websites__domain="sodavault.com"
        # ).prefetch_related('children', 'image_set').only(
            # 'title', 'excerpt', 'slug', 'parent'
        # ).order_by('menu_order', 'id')
        # return list_q

    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # return context


# class ArticleDetailView(BrCrumb, MetaData, Navigation, DetailView):

    # template_name = "blogapp/article_detail.html"

    # def dispatch(self, request, *args, **kwargs):
        # slug = self.kwargs["slug"]
        # article = Article.objects.prefetch_related('image_set').get(slug=slug)
        # self.images = {}
        # for image in article.image_set.all():
            # images = {}
            # check_featured = image.featured
            # if check_featured:
                # images['featured'] = image
            # self.images = images

        # self.queryset = article
        # self.mdata = article.mdata()
        # return super().dispatch(request, *args, **kwargs)

    # def get_object(self):
        # return self.queryset

    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context['images'] = self.images
        # return context


# class DocListView(BrCrumb, MetaData, Navigation, ListView):

    # template_name = "blogapp/doc_list.html"
    # paginate_by = 30

    # def get_queryset(self, *args, **kwargs):
        # list_q = Doc.objects.filter(
            # status="PUBLI",
            # parent__isnull=True,
            # websites__domain="sodavault.com"
        # ).prefetch_related('children', 'image_set').only(
            # 'title', 'excerpt', 'slug', 'parent'
        # ).order_by('menu_order', 'id')
        # return list_q

    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # return context


# class DocDetailView(BrCrumb, MetaData, Navigation, DetailView):

    # template_name = "blogapp/doc_detail.html"

    # def dispatch(self, request, *args, **kwargs):
        # slug = self.kwargs["slug"]
        # doc = Doc.objects.prefetch_related('image_set').get(slug=slug)
        # self.images = {}
        # for image in doc.image_set.all():
            # images = {}
            # check_featured = image.featured
            # if check_featured:
                # images['featured'] = image
            # self.images = images

        # self.queryset = doc
        # self.mdata = doc.mdata()
        # return super().dispatch(request, *args, **kwargs)

    # def get_object(self):
        # return self.queryset

    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context['images'] = self.images
        # return context


# class PageListView(BrCrumb, MetaData, Navigation, ListView):

    # template_name = "blogapp/page_list.html"
    # paginate_by = 30

    # def get_queryset(self, *args, **kwargs):
        # list_q = Page.objects.filter(
            # status="PUBLI",
            # parent__isnull=True,
            # websites__domain="sodavault.com"
        # ).prefetch_related('children', 'image_set').only(
            # 'title', 'excerpt', 'slug', 'parent'
        # ).order_by('menu_order', 'id')
        # return list_q

    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # return context


# class PageDetailView(BrCrumb, MetaData, Navigation, DetailView):

    # template_name = "blogapp/page_detail.html"

    # def dispatch(self, request, *args, **kwargs):
        # slug = self.kwargs["slug"]
        # page = Page.objects.prefetch_related('image_set').get(slug=slug)
        # self.images = {}
        # for image in page.image_set.all():
            # images = {}
            # check_featured = image.featured
            # if check_featured:
                # images['featured'] = image
            # self.images = images

        # self.queryset = page
        # self.mdata = page.mdata()
        # return super().dispatch(request, *args, **kwargs)

    # def get_object(self):
        # return self.queryset

    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context['images'] = self.images
        # return context


# # ########################
# # these can be done better
# # ########################
# class CategoryListView(BrCrumb, MetaData, Navigation, ListView):

    # model = Article
    # template_name = "blogapp/article_list.html"
    # paginate_by = 30

    # def get_queryset(self):
        # cat_id = self.kwargs["category_id"]
        # queryset = Article.objects.filter(topics__id=cat_id, status="PUBLI")
        # return queryset

    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context["context"] = context
        # context['robots'] = 'no'
        # return context


# class TagListView(BrCrumb, MetaData, Navigation, ListView):

    # model = Article
    # paginate_by = 30
    # template_name = "blogapp/article_list.html"

    # def get_queryset(self):
        # tag_id = self.kwargs["tag_id"]
        # queryset = Article.objects.filter(interests__id=tag_id, status="PUBLI")
        # return queryset

    # def get_context_data(self, **kwargs):
        # context = super(TagListView, self).get_context_data(**kwargs)
        # context["context"] = context
        # context['robots'] = 'no'
        # return context


# class DocSearchListView(BrCrumb, MetaData, Navigation, ListView):

    # model = Doc
    # paginate_by = 30
    # template_name = "blogapp/article_list.html"
    # http_method_names = ["get"]

    # def get_queryset(self):
        # search_query = self.request.GET.get("search_box", None)
        # if len(search_query) < 4:
            # queryset = Doc.objects.none()
        # else:
            # queryset = Doc.objects.filter(
                # Q(post_type="ARTICLE")
                # & (
                    # Q(keyword_list__icontains=search_query)
                    # | Q(title__icontains=search_query)
                    # | Q(excerpt__icontains=search_query)
                # )
            # ).exclude(Q(status="DRAFT") | Q(status="TRASH"))
        # return queryset

    # def get_context_data(self, **kwargs):
        # context = super(DocSearchListView, self).get_context_data(**kwargs)
        # context["context"] = context
        # context['robots'] = 'no'
#         return context
