from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.Form):
    email = forms.EmailField()
    Login = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    second_name = forms.CharField(max_length=100)
    third_name = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput())

    def clean_login(self):
        if User.objects.filter(Login=self.cleaned_data['Login']).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует:(')
        return self.cleaned_data['Login']

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует:(')
        return self.cleaned_data['email']
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password_confirmation'):
            raise forms.ValidationError('Пароли не совпадают:(')
        return self.cleaned_data


class SignInForm(forms.Form):
    Login = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())