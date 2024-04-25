from django import forms
from .models import Image

# image upload form
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("name", "Image_description", "img", "Image_category")


