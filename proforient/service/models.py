from django.db import models
from specialist.models import SpecialistProfile
from modelUtils.emailSignInModel import EmailSignInUser

class CategoriesManager(models.Manager):

    def allCategories(self):
        return self.all()


class Categories(models.Model):

    objects = CategoriesManager()

    name = models.CharField(max_length=70)


class CommentsManager(models.Manager):
    def allComments(self):
        return self.all()

class Comments(models.Model):

    objects = CommentsManager()

    author = models.ForeignKey(EmailSignInUser, on_delete=models.CASCADE)
    service = models.ForeignKey('Services', on_delete=models.CASCADE) # используется имя 'Service' потому что объект модели не объявлен
    text = models.TextField(max_length=2000)
    commentDate = models.DateTimeField(auto_now_add=True)



class ServiceManager(models.Manager):

    def allServices(self):
        return self.all()

    def allServicesByCategory(self,categoryName):
        return self.filter(categories__name=categoryName)

    def createService(self, newAuthor, newCategory, newTitle, newDescription, newPrice, avatar):
        serv =  Services()
       
        serv.author = newAuthor
        serv.category = newCategory
        serv.title = newTitle
        serv.description = newDescription
        serv.price = newPrice
        serv.avatar = avatar
        serv.save()
        return serv

    def allServicesByAuthor(self, userId):
        return self.filter(author__user_id=userId)
    
    def allBoughtServices(self, userId):
        return self.filter(buyer__id=userId)

        

class Services(models.Model):

    objects = ServiceManager()

    author = models.ForeignKey(SpecialistProfile, on_delete=models.CASCADE)
    buyer = models.ForeignKey(EmailSignInUser, on_delete=models.CASCADE,null=True)
    
    category = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=1000)
    price = models.IntegerField(default=0)
    buyerCnt = models.IntegerField(default=0)
    creationDate = models.DateField(auto_now_add=True)
    avatar = models.ImageField(upload_to='photos', null=True)


