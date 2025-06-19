from django import forms
from .models import PQRS, RespuestaPQRS

class PQRSForm(forms.ModelForm):
    class Meta:
        model = PQRS
        fields = ['tipo', 'titulo', 'descripcion']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto de la PQRS'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe detalladamente tu petición, queja, reclamo o sugerencia'})
        }
        labels = {
            'tipo': 'Tipo de PQRS',
            'titulo': 'Asunto',
            'descripcion': 'Descripción'
        }

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if not titulo or not titulo.strip():
            raise forms.ValidationError('Por favor llenar el campo.')
        return titulo

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if not descripcion or not descripcion.strip():
            raise forms.ValidationError('Por favor llenar el campo.')
        return descripcion

class RespuestaPQRSForm(forms.ModelForm):
    class Meta:
        model = RespuestaPQRS
        fields = ['mensaje']
        widgets = {
            'mensaje': forms.Textarea(attrs={'class': 'form-control'}),
        }
