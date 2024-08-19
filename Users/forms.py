from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordResetForm,SetPasswordForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'style': 'width: 100%'})
        self.fields['email'].widget.attrs.update({'style': 'width: 100%'})
        self.fields['password1'].widget.attrs.update({'style': 'width: 100%'})
        self.fields['password2'].widget.attrs.update({'style': 'width: 100%'})

class UserLoginForm(AuthenticationForm):
    
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'style': 'width: 100%'})
        self.fields['password'].widget.attrs.update({'style': 'width: 100%'})

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
    
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'style': 'width: 100%'})
        self.fields['email'].widget.attrs.update({'style': 'width: 100%'})


class UserPasswordResetForm(PasswordResetForm):
    
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'style': 'width: 100%'})


class UserSetPasswordForm(SetPasswordForm):
    
    def __init__(self, *args, **kwargs):
        super(UserSetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'style': 'width: 100%'})
        self.fields['new_password2'].widget.attrs.update({'style': 'width: 100%'})
