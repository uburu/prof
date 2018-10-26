from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.http import Http404


from specialist.forms import SignUpForm, SignInForm, ChangeSettingsForm
from specialist.models import SpecialistProfile
from user.models import Profile

def specialistSignUp(request):
    if request.method == 'GET':
        form = SignUpForm()
    elif request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            specialist = SpecialistProfile.objects.create_user(
                Login = form.cleaned_data['Login'],
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password'],
                first_name = form.cleaned_data['first_name'],
                second_name = form.cleaned_data['second_name'],
                third_name = form.cleaned_data['third_name']
            )
            login(request, specialist.user)
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'specialist_signup.html', context)

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
        'specialist': specialist
    }
    return render(request, 'specialist_profile.html', context)

@login_required
def specialistSettings(request):
    if request.user is None or request.user.id is None:
        raise Http404
    specialist = SpecialistProfile.objects.get(user_id=request.user.id)

    # initial - форма заполняется при загрузке. ключ - имя поля в форме. (все равно что <intput value="значение">)
    # заполнить форму исходными данными нужно для того, чтобы поля которые пользователь не изменял не заполнились None
    if request.method == 'GET':
        form = ChangeSettingsForm(initial={
            'email': specialist.user.email,
            'Login': specialist.user.username,
            'first_name': specialist.first_name,
            'second_name': specialist.second_name,
            'third_name': specialist.third_name,
            'education': specialist.education,
            'workExpirience': specialist.workExpirience,
            'about_me': specialist.about_me
        })
    elif request.method == 'POST':
        form = ChangeSettingsForm(request.POST)
        if form.is_valid():
            specialist.user.email = form.cleaned_data['email']
            specialist.user.username = form.cleaned_data['Login']
            specialist.first_name = form.cleaned_data['first_name']
            specialist.second_name = form.cleaned_data['second_name'] 
            specialist.third_name = form.cleaned_data['third_name']
            specialist.education = form.cleaned_data['education']
            specialist.workExpirience = form.cleaned_data['workExpirience'] 
            specialist.about_me = form.cleaned_data['about_me']
            specialist.user.save()
            specialist.save()
            return redirect('specialistProfile')
    context = {
        'form': form
    }
    return render(request, 'specialist_settings.html', context)

def showSomeProfile(request, id):
    # если пользователь вошел как специалист
    if SpecialistProfile.objects.filter(user_id=id).exists():
        specialist = SpecialistProfile.objects.get(user_id=id)
        context = {
            'specialist': specialist, 
        }
        return render(request, 'specialist_profile.html', context)
    # если пользователь зашел как студент
    elif Profile.objects.filter(user_id=id).exists():
        student = Profile.objects.get(user_id=id)
        context = {
            'student': student,
        }
        return render(request, 'student_profile.html', context)

# TODO в specialistProfile сделать проверки на DoesNotExist пользователя