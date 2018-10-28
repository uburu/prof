from django import forms
from django.contrib.auth.models import User # заменен на EmailSignInUser
from modelUtils.emailSignInModel import EmailSignInUser


class CreateServiceForm(forms.Form):
    category = forms.CharField(max_length=250)
    title = forms.CharField(max_length=250)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.IntegerField()

    def clean_price(self):
        if self.cleaned_data['price'] < 0:
            raise forms.ValidationError('Цена не может быть меньше нуля:(')
        return self.cleaned_data['price']

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data 
