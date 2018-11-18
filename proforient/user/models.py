from django.db import models
from django.contrib.auth.models import User # заменен на EmailSignInUser
from django.core.exceptions import ObjectDoesNotExist
from modelUtils.emailSignInModel import EmailSignInUser # кастомный User для аутентификации

# Create your models here.

class ProfileManager(models.Manager):

    def create_user(self, Login, email, password, first_name, second_name, third_name, avatar):
        user = EmailSignInUser.objects.create_user(Login, email, password) 
        return self.create(user=user, first_name=first_name, second_name=second_name, third_name=third_name, avatar=avatar,is_specialist=False)



class Profile(models.Model):
    objects = ProfileManager()
    user = models.OneToOneField(EmailSignInUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default=None)
    second_name = models.CharField(max_length=100, default=None)
    third_name = models.CharField(max_length=100, default=None)
    education = models.TextField(default=None, null=True)
    dreamWork = models.TextField(default=None, null=True)
    about_me = models.TextField(default=None, null=True)
    avatar = models.ImageField(upload_to='photos', null=True)
    is_specialist = models.BooleanField(default=False)