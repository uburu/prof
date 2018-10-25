from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signUp, name='signUp'),
    path('signin/', views.signIn, name='signIn'),
    path('signout/', views.signOut, name='signOut'),
    path('profile/', views.studentProfile, name='studentProfile'),
    path('student_settings/', views.studentSettings, name='studentSettings')

]
