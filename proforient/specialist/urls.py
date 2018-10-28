from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('specialist_signup/', views.specialistSignUp, name='specialistSignUp'),
    path('specialist_profile/', views.specialistProfile, name='specialistProfile'),
    path('specialist_settings/', views.specialistSettings, name='specialistSettings'),
    path('user/<int:id>', views.showSomeProfile, name='showSomeProfile')
]