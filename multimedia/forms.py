from django import forms
from .models import Image
# from multiupload.fields import MultiImageField
# from .fields import ValidatedMultiImageField


class CreateImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image',]
        widgets = {
            'image' : forms.ClearableFileInput(
                attrs={'multiple': '', 'accept': 'image/png, image/jpg, image/jpeg'}
            ),
        }

    #def clean_image(self):



class CreateVideoForm(forms.Form):
    video = forms.FileField(
        required=False, widget=forms.ClearableFileInput(
            attrs={
                'multiple': '', 'accept': 'video/mp4, video/avi'
            }
        )
    )