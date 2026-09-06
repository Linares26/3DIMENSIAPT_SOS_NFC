"""
3DimensiaPT - Sistema de Llaveros NFC de Emergencia
Archivo: emergencias/forms.py
"""
from django import forms
from .models import LlaveroNFC


class FichaEmergenciaForm(forms.ModelForm):
    """
    Formulário otimizado para pais com estilos nativos do Tailwind CSS
    e validação para uma atualização rápida em dispositivos móveis.
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
                'placeholder': 'Ej. Tiago'
            }),
            'apellidos_menor': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none focus:ring-2 focus:ring-rose-500/20 text-sm font-semibold',
                'placeholder': 'Ej. Pereira Silva'
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
                'placeholder': 'Ej. Mãe'
            }),
            'telefono_contacto_1': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-rose-300 bg-rose-50/40 px-3 py-2 text-slate-900 font-mono font-bold shadow-sm focus:border-rose-500 focus:outline-none text-xs',
                'placeholder': '+351 900 000 000'
            }),

            # Contacto Secundario SOS
            'nombre_contacto_2': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none text-xs font-semibold',
                'placeholder': 'Ej. Tiago Pereira (Pai)'
            }),
            'parentesco_contacto_2': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none text-xs',
                'placeholder': 'Ej. Pai / Avô'
            }),
            'telefono_contacto_2': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-slate-900 font-mono shadow-sm focus:border-rose-500 focus:outline-none text-xs',
                'placeholder': '+351 930 000 000'
            }),

            # Información Médica
            'grupo_sanguineo': forms.Select(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none text-xs font-bold'
            }),
            'alergias_graves': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full rounded-xl border border-rose-300 bg-rose-50/30 p-3 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none text-xs font-bold',
                'placeholder': 'Ex.: ALERGIA GRAVE A FRUTOS SECOS (amendoins, nozes) e PENICILINA.'
            }),
            'enfermedades_condiciones': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full rounded-xl border border-slate-300 bg-white p-3 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none text-xs',
                'placeholder': 'Ex.: Asma infantil com broncoespasmos estacionais.'
            }),
            'medicacion_urgencia': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none text-xs font-semibold',
                'placeholder': 'Ex.: Ventolín / Epipen na mochila escolar'
            }),
            'observaciones_medicas': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full rounded-xl border border-slate-300 bg-white p-3 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none text-xs',
                'placeholder': 'Qualquer detalhe extra que um médico ou policial precise saber.'
            }),
            'esta_activo': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 rounded border-slate-300 text-rose-600 focus:ring-rose-500 cursor-pointer'
            })
        }

    def clean_telefono_contacto_1(self):
        tel = self.cleaned_data.get('telefono_contacto_1')
        if not tel:
            raise forms.ValidationError("O telefone de emergência principal é obrigatório.")
        return tel.strip().replace(" ", "")
