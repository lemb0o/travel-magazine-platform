from django import forms
from .models import Travel


class CreateTravelForm(forms.ModelForm):
    class Meta:
        model = Travel
        fields = ['title', 'description', 'start', 'end', 'location', 'price', 'limit', 'has_offer', 'offer']
