from django.views.generic import ListView
# from .models import Product  # , Attribute, Term
# from .forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import (
        ListView, CreateView, UpdateView, DeleteView)
# from django.urls import reverse
from homeapp.mixins.navigation import Navigation


class ProductHomeView(LoginRequiredMixin, Navigation, TemplateView):
    template_name = 'productapp/product_home.html'
    pass


# class ProductListView(ListView):
    # model = Product
    # # form_class = CampaignForm
    # # success_message = "successfully created"

# class ProductCreateView(CreateView):
    # model = Product
    # form_class = ProductForm

    # def get_success_url(self):
        # return reverse('product-list')

# class ProductUpdateView(UpdateView):
    # model = Product
    # form_class = ProductForm

    # def get_success_url(self):
        # return reverse('product-list')

# class ProductDeleteView(DeleteView):
    # model = Product
    # form_class = ProductForm

    # def get_success_url(self):
        # return reverse('product-list')

