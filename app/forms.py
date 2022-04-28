from django import forms
from .models import images

class ImageForm(forms.ModelForm):
 class Meta:
  model = images
  fields = '__all__'
  labels = {'photo':''}