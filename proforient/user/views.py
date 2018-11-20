from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.http import Http404


from user.forms import SignUpForm, SignInForm, ChangeSettingsForm
from user.models import Profile
from viewUtils.paginate import _paginate

def studentSignUp(request):
    if request.method == 'GET':
        form = SignUpForm()
    elif request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            print(form)
            print(form.cleaned_data['avatar'])
            profile = Profile.objects.create_user(
                Login = form.cleaned_data['Login'],
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password'],
                first_name = form.cleaned_data['first_name'],
                second_name = form.cleaned_data['second_name'],
                third_name = form.cleaned_data['third_name'],
                avatar = form.cleaned_data['avatar']
            )
            login(request, profile.user)
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'user/student_signup.html', context)


#TODO валидировать успешность входа можно на уровне формы чтобы можно было рейзить ошибку и показывать ее сразу на фронте
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


#TODO сделать проверки на то что если пользователь хочет посмотреть не свой профиль студента(как во вьюхе specialist)
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
    if request.user is None or request.user.id is None: # TODO если пользователь незалогинен показывать сообщение а не 404
        raise Http404
    student = Profile.objects.get(user_id=request.user.id)
    if request.method == 'GET':
        form = ChangeSettingsForm()
    elif request.method == 'POST':
        form = ChangeSettingsForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            student.changeUserData(form.harvestingFormdata())
            return redirect('studentProfile')

    context = {
        'current_usr': student,
        'form': form,
        'student': student
    }
    print(form)
    return render(request, 'user/_student_settings.html', context)


        

# TODO в studentProfile сделать проверки на DoesNotExist пользователя