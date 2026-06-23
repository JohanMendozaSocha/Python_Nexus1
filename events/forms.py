from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        # Pedimos todo menos el creador y la fecha de creación
        fields = ['titulo', 'descripcion', 'ubicacion', 'f_inicio', 'f_fin', 'categoria']
        
        # Les ponemos widgets para que en el HTML salgan como cajas de texto y calendario
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del evento'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': '¿De qué trata el evento?'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lugar o enlace virtual'}),
            'f_inicio': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'f_fin': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Deportes, Tecnología...'}),
        }