from django import forms
from .models import Pacient

class FormularPacient(forms.ModelForm):
    class Meta:
        model = Pacient
        fields = '__all__'
        widgets = {
            'Sex': forms.Select(
                choices=((1, 'Bărbat'), (2, 'Femeie')),
                attrs={'style': 'width: 100%;'}
            ),
            'Colesterol': forms.Select(
                choices=((1, 'Normal'), (2, 'Above Normal'), (3, 'Well Above Normal')),
                attrs={'style': 'width: 100%;'}
            ),
            'Glucoză': forms.Select(
                choices=((1, 'Normal'), (2, 'Above Normal'), (3, 'Well Above Normal')),
                attrs={'style': 'width: 100%;'}
            ),
            'Fumător': forms.Select(
                choices=((0, 'Nu'), (1, 'Da')),
                attrs={'style': 'width: 100%;'}
            ),
            'Băutor': forms.Select(
                choices=((0, 'Nu'), (1, 'Da')),
                attrs={'style': 'width: 100%;'}
            ),
            'Activitate': forms.Select(
                choices=((0, 'Nu'), (1, 'Da')),
                attrs={'style': 'width: 100%;'}
            ),
            'NSS': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'Prenume': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'Nume': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'Email': forms.EmailInput(attrs={'style': 'width: 100%;'}),
            'Vârstă': forms.NumberInput(attrs={'style': 'width: 100%;'}),
            'Înălțime': forms.NumberInput(attrs={'style': 'width: 100%;'}),
            'Greutate': forms.NumberInput(attrs={'style': 'width: 100%;'}),
            'TAS': forms.NumberInput(attrs={'style': 'width: 100%;'}),
            'TAD': forms.NumberInput(attrs={'style': 'width: 100%;'}),
            'Risc_Boală': forms.NumberInput(attrs={'style': 'width: 100%;'}),
            'Dată_Adăugare': forms.DateInput(attrs={'style': 'width: 100%;'}),
        }