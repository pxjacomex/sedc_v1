from django import forms
from uploads.core.models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Estacion
        fields = ('est_nombre', 'est_ficha', )
