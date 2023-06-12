from django import forms
from .models import Place


class CreatePlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['name', 'description', 'location']
