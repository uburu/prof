from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User # заменен на EmailSignInUser
from django.core.exceptions import ObjectDoesNotExist
# from service.models import Services
from modelUtils.emailSignInModel import EmailSignInUser

# Create your models here.

class SpecialistProfileManager(models.Manager):

    def create_user(self, Login, email, password, first_name, second_name, third_name):
        user = EmailSignInUser.objects.create_user(Login, email, password) 
        return self.create(user=user, first_name=first_name, second_name=second_name, third_name=third_name,is_specialist=True)

    # def allBoughtServices(self):
    #     return self.myServices.all()


class SpecialistProfile(models.Model):
    objects = SpecialistProfileManager()
    user = models.OneToOneField(EmailSignInUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default=None)
    second_name = models.CharField(max_length=100, default=None)
    third_name = models.CharField(max_length=100, default=None)
    education = models.TextField(default=None, null=True)
    workExpirience = models.TextField(default=None, null=True)
    about_me = models.TextField(default=None, null=True)

    # myServices = models.ForeignKey(Services, on_delete=models.CASCADE)
    is_specialist = models.BooleanField(default=True)
