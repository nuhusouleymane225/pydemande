from django import forms
from django.forms import  *
from django.forms.models import ModelForm
from django.forms.widgets import *
from .models import Demande

    
class DemandeTraitementForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(DemandeTraitementForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['code_vehicule'].required = False
        self.fields['code_remorque'].required = False
        self.fields['imat_vehicule'].required = False
        self.fields['imat_remorque'].required = False
        self.fields['code_activite'].required = False
        self.fields['libelle_activite'].required = False
         


    class Meta:
        model = Demande
        exclude = ['user', 'ref_code', 'traite', 'soumis', 'items', 'agence', 'axe_analyse', 'qrcode', 'demande_date', 'montant_ttc']
        widgets={

            'num_releve': TextInput(attrs={'Placeholder': 'Numéro de relevé', 'class': 'form-control', 'autocomplete': 'off'}),
            'chauffeur': Select(attrs={'Placeholder': 'Chauffeur', 'class': 'form-control'}),
            'frais_date': DateInput(attrs={'type':'date', "format": "dd/mm/yyyy", 'class': 'form-control'}),
            
           
            
            'code_activite ': Select(attrs={'class': 'form-control'}),
            
            
            'libelle_activite': Select(attrs={'class': 'form-control'}),
            
            'a_rembourser':  CheckboxInput

        } 




##class DemandeRForm(ModelForm):
#    #num_releve = forms.CharField(widget=forms.TextInput(attrs={
#    #    'class': 'form-control',
#    #    'placeholder': 'Numéro de relevé',
#    #}))
#    code_vehicule = forms.CharField(required=False, widget=forms.TextInput(attrs={
#        'class': 'form-control',
#        'placeholder': 'code véhicule',
#    }))
#    code_remorque = forms.CharField(required=False, widget=forms.TextInput(attrs={
#        'class': 'form-control',
#        'placeholder': 'code remorque',
#    }))
#    imat_véhicule = forms.CharField(required=False, widget=forms.TextInput(attrs={
#        'class': 'form-control',
#        'placeholder': 'Imat. véhicule',
#    }))
#    imat_remorque = forms.CharField(required=False, widget=forms.TextInput(attrs={
#        'class': 'form-control',
#        'placeholder': 'Imat. remorque',
#    }))
#    
#    frais_date = forms.DateField()
#    a_rembourser = forms.BooleanField(required=False, widget=forms.CheckboxInput)
#    libelle_activite = forms.MultipleChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'default':'Choisir activité'}), choices=directionActChoix)
#    code_activite = forms.MultipleChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'default':'Choisir activité'}), choices=codeActivite)
#    ref_code = forms.CharField(required=False)
#    
#
#
#    class Meta:
#        model = Demande
#        fields = '__all__'
#


class DemandeForm(ModelForm):
    class Meta:
        model = Demande
        exclude = ['traite', 'user', 'soumis', 'imat_vehicule', 'items', 'id', 'code_vehicule', 'code_remorque', 'imat_remorque', 'agence', 'axe_analyse']
        widgets={

            'num_releve': TextInput(attrs={'Placeholder': 'Numéro de relevé', 'class': 'form-control', 'autocomplete': 'off'}),
            'chauffeur': Select(attrs={'class': 'form-control'}),
            'date_demande': DateInput(attrs={'type':'date', 'class': 'form-control'}),
            'frais_date': DateInput(attrs={'type':'date', 'class': 'form-control'}),
            'code_activite': Select(attrs={'class': 'form-control'}),
            'libelle_activite': Select(attrs={'class': 'form-control'}),
            'a_rembourser': CheckboxInput
        }