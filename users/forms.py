from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    # username = forms.CharField(label='Имя пользователя', widget=forms.TextInput)
    # email = forms.EmailField(label='Email', widget=forms.EmailInput)
    # password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     # Do whatever you want
    #     if error_case: # Write your own error case.
    #         raise forms.ValidationError("Error Message") # Your own error message that will appear to the user in case the field is not valid
    #     return username # In case everything is fine just return user's input.

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Введенная почта уже используется')
        return email




class UserRegistration(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Пароли не совпадают')
            return cd['password2']