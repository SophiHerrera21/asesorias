from django import forms
from .models import EntregaPrueba

class EntregaPruebaForm(forms.ModelForm):
    class Meta:
        model = EntregaPrueba
        fields = ['archivo', 'observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Observaciones adicionales (opcional)'}),
        }
        labels = {
            'archivo': 'Archivo de la prueba',
            'observaciones': 'Observaciones'
        } 