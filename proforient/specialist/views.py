from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from specialist.forms import SignUpForm, SignInForm, ChangeSettingsForm
from specialist.models import SpecialistProfile
from user.models import Profile
from service.models import Services
from modelUtils.emailSignInModel import EmailSignInUser
from modelUtils.userUtils import userDefine
from viewUtils.paginate import _paginate

def specialistSignUp(request):
    if request.method == 'GET':
        form = SignUpForm()
    elif request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES)
            print(form)
            print(form.cleaned_data['avatar'])
            specialist = SpecialistProfile.objects.create_user(
                Login = form.cleaned_data['Login'],
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password'],
                first_name = form.cleaned_data['first_name'],
                second_name = form.cleaned_data['second_name'],
                third_name = form.cleaned_data['third_name'],
                avatar = form.cleaned_data['avatar']
            )
            login(request, specialist.user)
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'specialist/specialist_signup.html', context)
    
def specialistSignIn(request):
    if request.method == 'GET':
        form = SignInForm()
    elif request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data['email'], # так как используем не дефолтного User, то аутентификация по email
                password=form.cleaned_data['password']
            )

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                context = {
                    'form': form
                }
                return render(request, 'unsuccess_signin.html', context)

    context= {
        'form': form
    }
    return render(request, 'specialist_signin.html', context)
    
@login_required
def specialistProfile(request):
    if request.user is None or request.user.id is None:
        raise Http404
    specialist = SpecialistProfile.objects.get(user_id=request.user.id)
    if not specialist.is_specialist:
        raise Http404
    context = {
        'current_usr': specialist,
        'usr': specialist,
        'is_me': True
    }
    return render(request, 'specialist/_specialist_profile.html', context)

@login_required
def specialistSettings(request):
    if request.user is None or request.user.id is None:
        raise Http404
    specialist = SpecialistProfile.objects.get(user_id=request.user.id)
    if request.method == 'GET':
        form = ChangeSettingsForm()
    elif request.method == 'POST':
        form = ChangeSettingsForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            specialist.changeUserData(form.harvestingFormdata())
            return redirect('specialistProfile')
    context = {
        'current_usr': specialist,
        'form': form,
        'specialist': specialist
    }
    return render(request, 'specialist/_specialist_settings.html', context)


# TODO показывать сообщение если пока у пользователя нет заказов или созданных услуг
@login_required
def myCreatedServices(request):
    current_usr = userDefine(request)
    myServices = _paginate(Services.objects.allServicesByAuthor(request.user.id), request)
    
    context = {
        'current_usr': current_usr,
        'services': myServices
    }
    return render(request, 'service/services.html', context)


# функция используемая для обоих user и specialists
@login_required
def myBoughtServices(request):
    current_usr = userDefine(request)
    print(list(Services.objects.allBoughtServices(request.user.id)))
    myServices = _paginate(Services.objects.allBoughtServices(request.user.id), request)
    
    context = {
        'current_usr': current_usr,
        'services': myServices
    }
    return render(request, 'service/bought_services.html', context)


def showSomeProfile(request, id):
    # получаем данные пользователя с которого хотим зайти на чью-то страницу
    current_usr = userDefine(request)

    # если пользователь хочет зайти не на свою страницу
    # то на страницу профиля передаем флаг и не показываем кнопки настроек и создания услуги
    if request.user.id != id:
        # если пользователь пытается зайти на страницу специалиста
        if SpecialistProfile.objects.filter(user_id=id).exists():
            specialist = SpecialistProfile.objects.get(user_id=id)
            context = {
                'current_usr': current_usr,
                'usr': specialist,
                'is_me': False 
            }
            return render(request, 'specialist/_specialist_profile.html', context)
        # если пользователь пытается зайти на страницу студента
        elif Profile.objects.filter(user_id=id).exists():
            student = Profile.objects.get(user_id=id)
            context = {
                'current_usr': current_usr,
                'usr': student,
                'is_me': False 
            }
            return render(request, 'user/_student_profile.html', context)
        else:
            raise ObjectDoesNotExist # говорим что пользователя не существует
    # если пользователь пытается зайти на свою страницу
    else: 
        # если пользователь является специалистом
        if SpecialistProfile.objects.filter(user_id=id).exists():
            specialist = SpecialistProfile.objects.get(user_id=id)
            context = {
                'current_usr': current_usr,
                'usr': specialist, 
                'is_me': True
            }
            return render(request, 'specialist/_specialist_profile.html', context)
        # если пользователь является студентом
        elif Profile.objects.filter(user_id=id).exists():
            student = Profile.objects.get(user_id=id)
            context = {
                'current_usr': current_usr,
                'usr': student,
                'is_me': True
            }
            return render(request, 'user/_student_profile.html', context)

# TODO в specialistProfile сделать проверки на DoesNotExist пользователя
