from django.db import models

from user.models import Profile
from specialist.models import SpecialistProfile
from service.models import Services

# Create your models here.

class StudentPhotosManager(models.Manager):
    def addPhoto(self, photo, user): 
        photoObj = StudentPhotos()
        photoObj.photo = photo
        photoObj.user = user
        photoObj.save()
    
    def allPhotosByStudent(self, studentId):
        return self.filter(user__user_id=studentId)


class StudentPhotos(models.Model):
    objects = StudentPhotosManager()
    photo = models.ImageField(upload_to='photos', null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)


class SpecialistPhotosManager(models.Manager):
    def addPhoto(self, photo, user): 
        photoObj = SpecialistPhotos()
        photoObj.photo = photo
        photoObj.user = user
        photoObj.save()

    def allPhotosBySpecialist(self, specialistId):
        return self.filter(user__user_id=specialistId)

class SpecialistPhotos(models.Model):
    objects = SpecialistPhotosManager()
    photo = models.ImageField(upload_to='photos', null=True)
    user = models.ForeignKey(SpecialistProfile, on_delete=models.CASCADE)

class ServicePhotosManager(models.Manager):
    def addPhoto(self, photo, service): 
        photoObj = SpecialistPhotos()
        photoObj.photo = photo
        photoObj.service = service
        photoObj.save()
    
    def allPhotosByService(self, serviceId):
        return self.filter(service__id=serviceId)

class ServicePhotos(models.Model):
    objects = ServicePhotosManager()
    photo = models.ImageField(upload_to='photos', null=True)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)