from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Profile


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Введенная почта уже используется')
        return email


class CustomUserChangeForm(forms.ModelForm):
    
    first_name = forms.CharField(initial='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя'
    }))

    last_name = forms.CharField(initial='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Фамилия'
    }))

    email = forms.CharField(initial='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Адрес электронной почты'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_first_name(self):
        cd = self.cleaned_data
        if not cd['first_name'].isalpha():
            raise forms.ValidationError('Введите имя')
        return cd['first_name']
    
    def clean_last_name(self):
        cd = self.cleaned_data
        if not cd['last_name'].isalpha():
            raise forms.ValidationError('Введите фамилию')
        return cd['last_name']

    def clean_email(self):
        email = self.cleaned_data['email']
        email_ = User.objects.filter(email=email)
        if email_.exists():
            if email_[0] != self.instance:
                raise forms.ValidationError('Введенная почта уже используется')
        return email


class ProfileEditForm(forms.ModelForm):
    bio = forms.CharField(initial='', widget=forms.Textarea(attrs={
        'rows': 3
    }))
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic']
