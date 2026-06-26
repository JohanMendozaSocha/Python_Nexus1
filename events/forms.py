from django import forms
from django.utils import timezone
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'descripcion', 'ubicacion', 'f_inicio', 'f_fin', 'categoria']
        
        labels = {
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'ubicacion': 'Ubicación',
            'f_inicio': 'Fecha y Hora de Inicio',
            'f_fin': 'Fecha y Hora de Finalización',
            'categoria': 'Categoría',
        }
        
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del evento'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe tu evento...'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lugar o enlace del evento'}),
            'f_inicio': forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'f_fin': forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Tecnología, Videojuegos'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['f_inicio'].input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M']
        self.fields['f_fin'].input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M']

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('f_inicio')
        fecha_fin = cleaned_data.get('f_fin')
        
        ahora = timezone.now()

        if fecha_inicio and timezone.is_naive(fecha_inicio):
            fecha_inicio = timezone.make_aware(fecha_inicio, timezone.get_current_timezone())
        if fecha_fin and timezone.is_naive(fecha_fin):
            fecha_fin = timezone.make_aware(fecha_fin, timezone.get_current_timezone())

        if fecha_inicio and fecha_inicio < ahora:
            self.add_error('f_inicio', "¡No puedes crear un evento en el pasado!")

        if fecha_fin and fecha_fin < ahora:
            self.add_error('f_fin', "El evento no puede terminar en el pasado.")

        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            self.add_error('f_fin', "La fecha de finalización no puede ser antes de la fecha de inicio.")

        return cleaned_data