from django import forms
from django.contrib.auth.models import User # заменен на EmailSignInUser
from modelUtils.emailSignInModel import EmailSignInUser


class SignUpForm(forms.Form):
    email = forms.EmailField()
    Login = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    second_name = forms.CharField(max_length=100)
    third_name = forms.CharField(max_length=100)
    avatar = forms.FileField(required=False)
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput())

    def clean_login(self):
        if EmailSignInUser.objects.filter(Login=self.cleaned_data['Login']).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует:(')
        return self.cleaned_data['Login']

    def clean_email(self):
        if EmailSignInUser.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует:(')
        return self.cleaned_data['email']
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password_confirmation'):
            self.add_error('password_confirmation', 'Пароли не совпадают:(')
        return self.cleaned_data


class SignInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class ChangeSettingsForm(forms.Form):
    email = forms.EmailField(required=False)
    Login = forms.CharField(max_length=100,required=False)
    first_name = forms.CharField(max_length=100,required=False)
    second_name = forms.CharField(max_length=100,required=False)
    third_name = forms.CharField(max_length=100,required=False)
    education = forms.CharField(max_length=1000,required=False,widget=forms.Textarea)
    dreamWork = forms.CharField(max_length=1000,required=False,widget=forms.Textarea)
    about_me = forms.CharField(max_length=1000,required=False,widget=forms.Textarea)
    avatar = forms.FileField(required=False)
    listOfPhotos = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    
    def harvestingFormdata(self):
        newData = {}
        for key in self.cleaned_data.keys():
            if key != 'listOfPhotos':
                if self.cleaned_data[key] != '' and self.cleaned_data[key] != None:
                    newData[key] = self.cleaned_data[key]
        return newData


