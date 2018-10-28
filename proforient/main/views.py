from django.shortcuts import render, redirect
from user.models import Profile
from specialist.models import SpecialistProfile



def index(request):

    # если пользователь вошел как специалист
    if SpecialistProfile.objects.filter(user__email=request.user).exists():
        specialist = SpecialistProfile.objects.get(user_id=request.user.id)
        context = {
            'current_usr': specialist, 
        }
        return render(request, 'index/index.html', context)
    # если пользователь зашел как студент
    elif Profile.objects.filter(user__email=request.user).exists():
        student = Profile.objects.get(user_id=request.user.id)
        context = {
            'current_usr': student,
        }
        return render(request, 'index/index.html', context)
    
    return render(request, 'index/index.html')