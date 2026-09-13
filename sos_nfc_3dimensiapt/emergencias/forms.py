"""
3DimensiaPT - Sistema de Llaveros NFC de Emergencia
Archivo: emergencias/forms.py
"""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import LlaveroNFC


class FichaEmergenciaForm(forms.ModelForm):
    """
    Formulário otimizado para pais com estilos nativos do Tailwind CSS
    e validação para uma atualização rápida em dispositivos móveis.
    """
    
    class Meta:
        model = LlaveroNFC
        fields = [
            _('nombre_menor'),
            _('apellidos_menor'),
            _('fecha_nacimiento'),
            _('foto'),
            _('nombre_contacto_1'),
            _('parentesco_contacto_1'),
            _('telefono_contacto_1'),
            _('nombre_contacto_2'),
            _('parentesco_contacto_2'),
            _('telefono_contacto_2'),
            _('grupo_sanguineo'),
            _('alergias_graves'),
            _('enfermedades_condiciones'),
            _('medicacion_urgencia'),
            _('observaciones_medicas'),
            _('esta_activo'),
        ]
        
        widgets = {
            'nombre_menor': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none focus:ring-2 focus:ring-rose-500/20 text-sm font-semibold',
                'placeholder': _('Ex: Tiago')
            }),
            'apellidos_menor': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none focus:ring-2 focus:ring-rose-500/20 text-sm font-semibold',
                'placeholder': _('Ex: Pereira Silva')
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
                'placeholder': _('Ex: Laura Gomes (Mãe)')
            }),
            'parentesco_contacto_1': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none text-xs',
                'placeholder': _('Ex: Mãe')
            }),
            'telefono_contacto_1': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-rose-300 bg-rose-50/40 px-3 py-2 text-slate-900 font-mono font-bold shadow-sm focus:border-rose-500 focus:outline-none text-xs',
                'placeholder': '+351 900 000 000'
            }),

            # Contacto Secundario SOS
            'nombre_contacto_2': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none text-xs font-semibold',
                'placeholder': _('Ex: Tiago Pereira (Pai)')
            }),
            'parentesco_contacto_2': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none text-xs',
                'placeholder': _('Ex: Pai / Avô')
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
                'placeholder': _('Ex.: ALERGIA GRAVE A FRUTOS SECOS (amendoins, nozes) e PENICILINA.')
            }),
            'enfermedades_condiciones': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full rounded-xl border border-slate-300 bg-white p-3 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none text-xs',
                'placeholder': _('Ex.: Asma infantil com broncoespasmos estacionais.')
            }),
            'medicacion_urgencia': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none text-xs font-semibold',
                'placeholder': _('Ex.: Ventolín / Epipen na mochila escolar')
            }),
            'observaciones_medicas': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full rounded-xl border border-slate-300 bg-white p-3 text-slate-900 shadow-sm focus:border-rose-500 focus:outline-none text-xs',
                'placeholder': _('Qualquer detalhe extra que um médico ou policial precise saber.')
            }),
            'esta_activo': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 rounded border-slate-300 text-rose-600 focus:ring-rose-500 cursor-pointer'
            })
        }

    def clean_telefono_contacto_1(self):
        tel = self.cleaned_data.get('telefono_contacto_1')
        if not tel:
            raise forms.ValidationError(_("O telefone de emergência principal é obrigatório."))
        return tel.strip().replace(" ", "")
