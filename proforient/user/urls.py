from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('student_signup/', views.studentSignUp, name='studentSignUp'),
    path('signin/', views.signIn, name='signIn'),
    path('signout/', views.signOut, name='signOut'),
    path('student_profile/', views.studentProfile, name='studentProfile'),
    path('student_settings/', views.studentSettings, name='studentSettings')
]
