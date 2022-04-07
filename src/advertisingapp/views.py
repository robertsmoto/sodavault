from .models import Campaign
from .forms import CampaignForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.views.generic import CreateView, UpdateView, DeleteView
from homeapp.mixins.navigation import Navigation
from django.urls import reverse


class AdvertisingView(LoginRequiredMixin, Navigation, TemplateView):
    template_name = 'advertisingapp/ads_home.html'
    pass


# class CampaignAutocomplete(autocomplete.Select2QuerySetView):
    # def get_queryset(self):
        # # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated:
            # return Campaign.objects.none()

        # qs = Campaign.objects.all()

        # if self.q:
            # qs = qs.filter(name__icontains=self.q)

#         return qs


class CampaignListView(ListView):
    model = Campaign
    # form_class = CampaignForm
    # success_message = "successfully created"


class CampaignCreateView(CreateView):
    model = Campaign
    form_class = CampaignForm
    success_message = "success: created campaign"

    def get_success_url(self):
        return reverse('campaign-list')


class CampaignUpdateView(UpdateView):
    model = Campaign
    form_class = CampaignForm

    def get_success_url(self):
        return reverse('campaign-list')


class CampaignDeleteView(DeleteView):
    model = Campaign
    form_class = CampaignForm

    def get_success_url(self):
        return reverse('campaign-list')


# class AssettView(LoginRequiredMixin, Navigation, FormView):
    # template_name = 'advertisingapp/assett.html'
    # form_class = AssettForm
    # success_url = 'core'
    # pass


# class BannerView(LoginRequiredMixin, Navigation, FormView):
    # template_name = 'advertisingapp/banner.html'
    # form_class = BannerForm
    # success_url = 'core'
#     pass

# from rest_framework import viewsets
# from rest_framework import permissions
# from .serializers import CampaignSerializer
# from django.db.models import Q
# from datetime import datetime


# class CampaignViewSet(viewsets.ModelViewSet):
    # """
    # API endpoint that allows campaign to be viewed or edited.
    # """
    # queryset = Campaign.objects.filter(
        # Q(date_expires__isnull=True) |
        # Q(date_expires__gte=datetime.now())
    # ).order_by('-date_added')
    # serializer_class = CampaignSerializer
    # permission_classes = [permissions.IsAuthenticated]


# class GroupViewSet(viewsets.ModelViewSet):
    # """
    # API endpoint that allows groups to be viewed or edited.
    # """
    # queryset = Group.objects.all()
    # serializer_class = GroupSerializer
    # permission_classes = [permissions.IsAuthenticated]

