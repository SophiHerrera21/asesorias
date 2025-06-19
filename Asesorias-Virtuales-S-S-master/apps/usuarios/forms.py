from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from .models import Usuario, Asesor

class UsuarioForm(UserCreationForm):
    ficha = forms.CharField(required=False, widget=forms.HiddenInput(), initial='SIN_FICHA')
    programa = forms.CharField(required=False, widget=forms.HiddenInput(), initial='SIN_PROGRAMA')
    trimestre = forms.ChoiceField(
        required=False,
        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')],
        widget=forms.HiddenInput(),
        initial='1'
    )
    cargo = forms.CharField(required=False, widget=forms.HiddenInput(), initial='Coordinador')
    departamento = forms.CharField(required=False, widget=forms.HiddenInput(), initial='General')
    
    class Meta:
        model = Usuario
        fields = [
            'first_name', 'last_name', 'email', 'documento',
            'role', 'telefono', 'direccion'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar widgets de contraseña
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        
        # Personalizar mensajes de ayuda
        self.fields['password1'].help_text = 'La contraseña debe tener al menos 5 caracteres.'
        self.fields['password2'].help_text = 'Ingresa la misma contraseña para verificación.'
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1 and len(password1) < 5:
            raise ValidationError('La contraseña debe tener al menos 5 caracteres.')
        return password1
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email
    
    def clean_documento(self):
        documento = self.cleaned_data.get('documento')
        if Usuario.objects.filter(documento=documento).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError('Este documento ya está registrado.')
        return documento

class SolicitarRecuperacionForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu correo'}))

class CodigoRecuperacionForm(forms.Form):
    codigo = forms.CharField(label='Código de recuperación', max_length=6, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código de 6 dígitos'}))

class NuevaContrasenaForm(forms.Form):
    nueva_contrasena = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nueva contraseña'}))
    confirmar_contrasena = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirma la contraseña'}))

    def clean(self):
        cleaned_data = super().clean()
        nueva = cleaned_data.get('nueva_contrasena')
        confirmar = cleaned_data.get('confirmar_contrasena')
        
        if nueva and len(nueva) < 5:
            raise ValidationError('La contraseña debe tener al menos 5 caracteres.')
        
        if nueva and confirmar and nueva != confirmar:
            raise ValidationError('Las contraseñas no coinciden.')
        return cleaned_data

class PerfilAprendizForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefono', 'direccion', 'imagen_perfil']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'imagen_perfil': forms.FileInput(attrs={'class': 'form-control'})
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'imagen_perfil': 'Foto de perfil'
        }

class AsesorRegistroForm(UsuarioForm):
    especialidad = forms.CharField(
        label='Especialidad',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Programación, Matemáticas'}),
        help_text='Área de especialización para asesorías'
    )

    class Meta(UsuarioForm.Meta):
        fields = UsuarioForm.Meta.fields + ['especialidad']
    
    def clean_especialidad(self):
        especialidad = self.cleaned_data.get('especialidad')
        if not especialidad or len(especialidad.strip()) < 3:
            raise ValidationError('La especialidad debe tener al menos 3 caracteres.')
        return especialidad.strip()

class AsesorPerfilForm(forms.ModelForm):
    class Meta:
        model = Asesor
        fields = ['especialidad', 'experiencia', 'titulo', 'disponibilidad']
        widgets = {
            'especialidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Programación, Matemáticas'}),
            'experiencia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe tu experiencia académica y profesional'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Ingeniero de Sistemas'}),
            'disponibilidad': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Horarios disponibles para asesorías'}),
        }
        labels = {
            'especialidad': 'Especialidad',
            'experiencia': 'Experiencia',
            'titulo': 'Título',
            'disponibilidad': 'Disponibilidad'
        }
        help_texts = {
            'experiencia': 'Describe tu experiencia en el área de especialidad',
            'titulo': 'Título académico obtenido',
            'disponibilidad': 'Indica tus horarios disponibles para asesorías'
        }
    
    def clean_especialidad(self):
        especialidad = self.cleaned_data.get('especialidad')
        if not especialidad or len(especialidad.strip()) < 3:
            raise ValidationError('La especialidad debe tener al menos 3 caracteres.')
        return especialidad.strip()
    
    def clean_experiencia(self):
        experiencia = self.cleaned_data.get('experiencia')
        if not experiencia or len(experiencia.strip()) < 10:
            raise ValidationError('La experiencia debe tener al menos 10 caracteres.')
        return experiencia.strip()
    
    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if not titulo or len(titulo.strip()) < 3:
            raise ValidationError('El título debe tener al menos 3 caracteres.')
        return titulo.strip()
    
    def clean_disponibilidad(self):
        disponibilidad = self.cleaned_data.get('disponibilidad')
        if not disponibilidad or len(disponibilidad.strip()) < 5:
            raise ValidationError('La disponibilidad debe tener al menos 5 caracteres.')
        return disponibilidad.strip() 