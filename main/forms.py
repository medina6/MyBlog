
from datetime import datetime

from django import forms

from .models import Apartment, Image



class ApartmentForm(forms.ModelForm):
    created = forms.DateTimeField(initial=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), required=False)
    class Meta:
        model = Apartment
        exclude = ('user', )

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', )



