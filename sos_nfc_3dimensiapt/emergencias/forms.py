"""
3DimensiaPT - Sistema de Llaveros NFC de Emergencia
Archivo: emergencias/forms.py
"""
from django import forms
from .models import LlaveroNFC


class FichaEmergenciaForm(forms.ModelForm):
    """
    Formulario optimizado para padres con estilos nativos de Tailwind CSS
    y validación para actualización rápida en dispositivos móviles.
    """
    
    class Meta:
        model = LlaveroNFC
        fields = [
            'nombre_menor',
            'apellidos_menor',
            'fecha_nacimiento',
            'foto',
            'nombre_contacto_1',
            'parentesco_contacto_1',
            'telefono_contacto_1',
            'nombre_contacto_2',
            'parentesco_contacto_2',
            'telefono_contacto_2',
            'grupo_sanguineo',
            'alergias_graves',
            'enfermedades_condiciones',
            'medicacion_urgencia',
            'observaciones_medicas',
            'esta_activo',
        ]
        
        widgets = {
            'nombre_menor': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none focus:ring-2 focus:ring-rose-500/20 text-sm font-semibold',
                'placeholder': 'Ej. Lucas'
            }),
            'apellidos_menor': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none focus:ring-2 focus:ring-rose-500/20 text-sm font-semibold',
                'placeholder': 'Ej. Martínez Gómez'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none focus:ring-2 focus:ring-rose-500/20 text-sm'
            }),
            'foto': forms.ClearableFileInput(attrs={
                'class': 'w-full text-xs text-slate-600 file:mr-3 file:py-2 file:px-3 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-rose-50 file:text-rose-700 hover:file:bg-rose-100 cursor-pointer',
                'accept': 'image/*'
            }),
            
            # Contacto Principal SOS
            'nombre_contacto_1': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none text-xs font-semibold',
                'placeholder': 'Ej. Laura Gómez (Mamá)'
            }),
            'parentesco_contacto_1': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none text-xs',
                'placeholder': 'Ej. Madre'
            }),
            'telefono_contacto_1': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-rose-300 bg-rose-50/40 px-3 py-2 text-slate-900 font-mono font-bold shadow-sm focus:border-rose-500 focus:outline-none text-xs',
                'placeholder': '+34 600 000 000'
            }),

            # Contacto Secundario SOS
            'nombre_contacto_2': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none text-xs font-semibold',
                'placeholder': 'Ej. Carlos Martínez (Papá)'
            }),
            'parentesco_contacto_2': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none text-xs',
                'placeholder': 'Ej. Padre / Abuelo'
            }),
            'telefono_contacto_2': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-slate-900 font-mono shadow-sm focus:border-rose-500 focus:outline-none text-xs',
                'placeholder': '+34 611 111 111'
            }),

            # Información Médica
            'grupo_sanguineo': forms.Select(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none text-xs font-bold'
            }),
            'alergias_graves': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full rounded-xl border border-rose-300 bg-rose-50/30 p-3 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none text-xs font-bold',
                'placeholder': 'Ej. ALERGIA SEVERA A FRUTOS SECOS (Cacahuetes, Nueces) y PENICILINA.'
            }),
            'enfermedades_condiciones': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full rounded-xl border border-slate-300 bg-white p-3 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none text-xs',
                'placeholder': 'Ej. Asma infantil con broncoespasmos estacionales.'
            }),
            'medicacion_urgencia': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none text-xs font-semibold',
                'placeholder': 'Ej. Ventolín / Epipen en la mochila escolar'
            }),
            'observaciones_medicas': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full rounded-xl border border-slate-300 bg-white p-3 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none text-xs',
                'placeholder': 'Cualquier detalle extra que deba saber un médico o policía.'
            }),
            'esta_activo': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 rounded border-slate-300 text-rose-600 focus:ring-rose-500 cursor-pointer'
            })
        }

    def clean_telefono_contacto_1(self):
        tel = self.cleaned_data.get('telefono_contacto_1')
        if not tel:
            raise forms.ValidationError("El teléfono de emergencia principal es obligatorio.")
        return tel.strip().replace(" ", "")
