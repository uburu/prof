from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('services/', views.allServicesPage, name='allServicesPage'),
    path('services/<slug:category_name>/', views.servicesByCategoryPage, name='servicesByCategoryPage'),
    path('service/<int:id>', views.servicePage, name='servicePage'),
    path('create_service/', views.createService, name='createService'),
    path('buy/<int:id>/', views.buyService, name='buyService')
]
