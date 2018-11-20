from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User # заменен на EmailSignInUser
from django.core.exceptions import ObjectDoesNotExist
# from service.models import Services
from modelUtils.emailSignInModel import EmailSignInUser

# Create your models here.

class SpecialistProfileManager(models.Manager):

    def create_user(self, Login, email, password, first_name, second_name, third_name, avatar):
        user = EmailSignInUser.objects.create_user(Login, email, password) 
        return self.create(user=user, first_name=first_name, second_name=second_name, third_name=third_name, avatar=avatar,is_specialist=True)

class SpecialistProfile(models.Model):
    objects = SpecialistProfileManager()

    user = models.OneToOneField(EmailSignInUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True)
    second_name = models.CharField(max_length=100, null=True)
    third_name = models.CharField(max_length=100, null=True)
    education = models.TextField(null=True)
    workExpirience = models.TextField(null=True)
    about_me = models.TextField(null=True)
    avatar = models.ImageField(upload_to='photos', null=True)
    is_specialist = models.BooleanField(default=True)

    def changeUserData(self, data):
        if data.get('email') and data['email'] != '':
            self.user.email = data.pop('email')
        if data.get('Login') and data['Login'] != '':
            self.user.username = data.pop('Login')
        for key in data.keys():
            self.__dict__[key] = data[key]
        self.user.save()
        self.save()
        return self
