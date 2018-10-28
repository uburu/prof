from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.http import Http404


from user.forms import SignUpForm, SignInForm, ChangeSettingsForm
from user.models import Profile

def studentSignUp(request):
    if request.method == 'GET':
        form = SignUpForm()
    elif request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            profile = Profile.objects.create_user(
                Login = form.cleaned_data['Login'],
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password'],
                first_name = form.cleaned_data['first_name'],
                second_name = form.cleaned_data['second_name'],
                third_name = form.cleaned_data['third_name']
            )
            login(request, profile.user)
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'user/student_signup.html', context)

def signIn(request):
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
    return render(request, 'user/student_signin.html', context)

@login_required
def signOut(request):
    logout(request)
    return redirect('/')

@login_required
def studentProfile(request):
    if request.user is None or request.user.id is None:
        raise Http404
    student = Profile.objects.get(user_id=request.user.id)
    context = {
        'current_usr': student,
        'usr': student,
        'is_me': True
    }
    return render(request, 'user/_student_profile.html', context)

@login_required
def studentSettings(request):
    if request.user is None or request.user.id is None:
        raise Http404
    student = Profile.objects.get(user_id=request.user.id)

    # initial - форма заполняется при загрузке. ключ - имя поля в форме. (все равно что <intput value="значение">)
    # заполнить форму исходными данными нужно для того, чтобы поля которые пользователь не изменял не заполнились None
    if request.method == 'GET':
        form = ChangeSettingsForm(initial={
            'email': student.user.email,
            'Login': student.user.username,
            'first_name': student.first_name,
            'second_name': student.second_name,
            'third_name': student.third_name,
            'education': student.education,
            'dreamWork': student.dreamWork,
            'about_me': student.about_me
        })
    elif request.method == 'POST':
        form = ChangeSettingsForm(request.POST)
        if form.is_valid():
            student.user.email = form.cleaned_data['email']
            student.user.username = form.cleaned_data['Login']
            student.first_name = form.cleaned_data['first_name']
            student.second_name = form.cleaned_data['second_name'] 
            student.third_name = form.cleaned_data['third_name']
            student.education = form.cleaned_data['education']
            student.dreamWork = form.cleaned_data['dreamWork'] 
            student.about_me = form.cleaned_data['about_me']
            student.user.save()
            student.save()
            return redirect('studentProfile')

    context = {
        'current_usr': student,
        'form': form
    }
    print(form)
    return render(request, 'user/_student_settings.html', context)



        

# TODO в studentProfile сделать проверки на DoesNotExist пользователя