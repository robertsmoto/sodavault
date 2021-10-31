from dal import autocomplete
from django import forms
from .models import Campaign, Assett, Banner


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ('__all__')


class AssettForm(forms.ModelForm):
    campaign = forms.ModelChoiceField(
        queryset=Assett.objects.all(),
        widget=autocomplete.ModelSelect2(url='campaign-autocomplete',
            attrs={
                # Set some placeholder
                'data-placeholder': 'Autocomplete ...',
                # Only trigger autocompletion after 3 characters have been typed
                # 'data-minimum-input-length': 3,
            },
        )
    )

    class Meta:
        model = Assett
        fields = ('__all__')


class BannerForm(forms.ModelForm):
    campaign = forms.ModelChoiceField(
        queryset=Assett.objects.all(),
        widget=autocomplete.ModelSelect2(
        url='campaign-autocomplete',
            attrs={
                # Set some placeholder
                'data-placeholder': 'Autocomplete ...',
                # Only trigger autocompletion after 3 characters have been typed
                # 'data-minimum-input-length': 3,
            },
        )
    )

    class Meta:
        model = Banner
        fields = ('__all__')
