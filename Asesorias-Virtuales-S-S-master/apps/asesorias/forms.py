from django import forms
from .models import Asesoria
from datetime import date

class AsesoriaForm(forms.ModelForm):
    class Meta:
        model = Asesoria
        fields = ['grupo', 'componente', 'fecha', 'hora', 'link_videollamada']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'link_videollamada': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://meet.google.com/...'}),
        }

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha < date.today():
            raise forms.ValidationError('La fecha no puede ser anterior a hoy.')
        return fecha

    def clean_link_videollamada(self):
        link = self.cleaned_data['link_videollamada']
        if not link.startswith('https://meet.google.com/'):
            raise forms.ValidationError('El enlace debe ser de Google Meet (https://meet.google.com/...).')
        return link

    def clean_grupo(self):
        grupo = self.cleaned_data['grupo']
        if not hasattr(grupo, 'asesor') or not grupo.asesor or grupo.asesor.role != 'asesor':
            raise forms.ValidationError('El grupo debe tener un asesor válido.')
        return grupo 