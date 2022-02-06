from django.views.generic import ListView
from .models import Product  # , Attribute, Term
# from .models import ProductAttributeJoin, VariationAttribute, Variation
from .forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from homeapp.mixins import Navigation
from dal import autocomplete
from django.db.models import Q


class ProductHomeView(LoginRequiredMixin, Navigation, TemplateView):
    template_name = 'productapp/product_home.html' 
    pass


# # These views used for ATTRIBUTES
# class AttrAutocomplete(autocomplete.Select2QuerySetView):
    # def get_queryset(self):
        # # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated:
            # return Term.objects.none()

        # qs = Attribute.objects.all()

        # pid = self.forwarded.get('product', None)

        # if pid:
            # attrids = ProductAttributeJoin.objects.filter(product_id=pid).values_list('attribute_id')
            # qs = qs.exclude(id__in=attrids)

        # if self.q:
            # qs = qs.filter(name__icontains=self.q)

        # return qs

# class AttrTermAutocomplete(autocomplete.Select2QuerySetView):
    # def get_queryset(self):
        # # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated:
            # return Term.objects.none()

        # qs = Term.objects.all()

        # attribute = self.forwarded.get('attribute', None)
        # termids = self.forwarded.get('self', None)
        # print("\n\n")
        # print("attribute", attribute)
        # print("termids", termids)

        # if attribute:
            # qs = qs.filter(attribute=attribute[0]).exclude(id__in=termids)

        # if self.q:
            # qs = qs.filter(name__icontains=self.q)

        # return qs


# # These view used for VARIATIONS
# class VarAttrAutocomplete(autocomplete.Select2QuerySetView):
    # def get_queryset(self):
        # # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated:
            # return Attribute.objects.none()

        # qs = Attribute.objects.all()

        # # forwarded from widget
        # var_id = self.forwarded.get('variation', None)
        # print("\nvariation id", var_id)
        # var_obj = Variation.objects.get(id=var_id)
        # pid = var_obj.parent_id
        # print("\npid", pid)

        # if pid:
            # filter_ids = ProductAttributeJoin.objects.filter(product_id=pid).values_list('attribute_id')
            # print("\nfilter_ids", filter_ids)
            # qs = qs.filter(id__in=filter_ids)
            # print("\nqs", qs)

        # if self.q:
            # qs = qs.filter(attribute__name__icontains=self.q)

        # return qs

# class VarTermAutocomplete(autocomplete.Select2QuerySetView):
    # def get_queryset(self):
        # # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated:
            # return Attribute.objects.none()

        # qs = Term.objects.all()

        # # forwarded from widget
        # var_id = self.forwarded.get('variation', None)
        # print("\nvariation id", var_id)
        # var_obj = Variation.objects.get(id=var_id)
        # pid = var_obj.parent_id
        # print("\npid", pid)
        # attr_id = self.forwarded.get('attribute', None)

        # if pid:
             
            # filter_ids = ProductAttributeJoin.objects.filter(
                # Q(product_id=pid) & Q(attribute_id=attr_id)
            # ).values_list(
                # 'term__id')
            # qs = qs.filter(id__in=filter_ids)

        # if self.q:
            # qs = qs.filter(attribute__name__icontains=self.q)

        # return qs


class ProductListView(ListView):
    model = Product
    # form_class = CampaignForm
    # success_message = "successfully created"

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('product-list')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('product-list')

class ProductDeleteView(DeleteView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('product-list')

