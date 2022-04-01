from blogapp.models import Post
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.db.models import Q
from homeapp.mixins import Navigation
from docsapp.views import BrCrumb


class BlogListView(Navigation, ListView):

    template_name = "blogapp/page_list.html"
    paginate_by = 30

    def get_queryset(self, *args, **kwargs):
        post_type = 'DOCS'
        if "post_type" in self.kwargs:
            post_type = self.kwargs["post_type"]
        # post_val = Post.objects.values_list(
            # 'body', 'categories', 'excerpt', 'featured_image', 'footer',
            # 'image_caption', 'image_title', 'keyword_list', 'post_type', 
            # 'slug', 'tags', 'thumbnail_image', 'title'
        # )
        # post_q = Post.objects.get(slug=slug)
        # post_q.query = pickle.loads(pickle.dumps(post_val.query))
        list_q = Post.objects.filter(
            post_type=post_type,
            status="PUBLI",
            parent__isnull=True
        ).prefetch_related('children').only(
            'title', 'excerpt', 'slug', 'post_type', 'parent', 
            'image_featured', 'image_thumb'
        ).order_by('menu_order', 'id')
        return list_q

#     def get_template_names(self):
        # post_type = "article"
        # if "post_type" in self.kwargs:
            # post_type = self.kwargs["post_type"]

        # if post_type == "article":
            # template_name = "blogapp/article_list.html"
        # elif post_type == "editorial":
            # template_name = "blogapp/editorial_list.html"
        # else:
            # template_name = "blogapp/page_list.html"
        # return template_name

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        post_type = "article"
        if "post_type" in self.kwargs:
            post_type = self.kwargs["post_type"]
        context["context"] = context
        context["post_type"] = post_type
        return context

# class PostListView(
    # BrCrumb, Navigation, MetaData, ListView
# ):

    # paginate_by = 30

    # def get_queryset(self, *args, **kwargs):
        # post_type = self.kwargs["post_type"].upper()
        # queryset = Post.objects.filter(post_type=post_type, status="PUBLI")
        # return queryset

    # def get_template_names(self):
        # post_type = self.kwargs["post_type"]
        # if post_type == "article":
            # template_name = "blogapp/article_list.html"
        # elif post_type == "editorial":
            # template_name = "blogapp/editorial_list.html"
        # else:
            # template_name = "blogapp/page_list.html"
        # return template_name

    # def get_context_data(self, **kwargs):
        # context = super(PostListView, self).get_context_data(**kwargs)
        # context["context"] = context
        # context["post_type"] = self.kwargs["post_type"]
        # return context


class BlogDetailView(Navigation, DetailView):

    template_name = "blogapp/page_detail.html"

    def get_object(self):
        slug = self.kwargs["slug"]
        queryset = Post.objects.prefetch_related('image_set').get(slug=slug)
        for image in queryset.image_set.all():
            images = {}
            check_featured = image.__dict__.get('featured', '')
            if check_featured:
                images['featured'] = image.__dict__
            order = image.__dict__.get('order', 0)
            images[order] = image.__dict__
            print("###images", images)

        self.images = images
        return queryset

    # def get_template_names(self):
        # post_type = self.kwargs["post_type"]
        # if post_type == "article":
            # template_name = "blogapp/article_detail.html"
        # elif post_type == "editorial":
            # template_name = "blogapp/editorial_detail.html"
        # else:
            # template_name = "blogapp/page_detail.html"
        # return template_name

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context['context'] = context
        context['images'] = self.images
        # context["metadata"] = Post.metadata_func(self)
        context['post_type'] = self.kwargs['post_type']
        return context


class CategoryListView(BrCrumb, Navigation, ListView):

    model = Post
    template_name = "blogapp/article_list.html"
    paginate_by = 30

    def get_queryset(self):
        cat_id = self.kwargs["category_id"]
        queryset = Post.objects.filter(topics__id=cat_id, status="PUBLI")
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context["context"] = context
        context['robots'] = 'no'
        return context


class TagListView(BrCrumb, Navigation, ListView):

    model = Post
    paginate_by = 30
    template_name = "blogapp/article_list.html"

    def get_queryset(self):
        tag_id = self.kwargs["tag_id"]
        queryset = Post.objects.filter(interests__id=tag_id, status="PUBLI")
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        context["context"] = context
        context['robots'] = 'no'
        return context


class DocSearchListView(BrCrumb, Navigation, ListView):

    model = Post
    paginate_by = 30
    template_name = "blogapp/article_list.html"
    http_method_names = ["get"]

    def get_queryset(self):
        search_query = self.request.GET.get("search_box", None)
        if len(search_query) < 4:
            queryset = Post.on_site.none()
        else:
            queryset = Post.objects.filter(
                Q(post_type="ARTICLE")
                & (
                    Q(keyword_list__icontains=search_query)
                    | Q(title__icontains=search_query)
                    | Q(excerpt__icontains=search_query)
                )
            ).exclude(Q(status="DRAFT") | Q(status="TRASH"))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(DocSearchListView, self).get_context_data(**kwargs)
        context["context"] = context
        context['robots'] = 'no'
        return context
