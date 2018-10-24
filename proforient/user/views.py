from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.http import Http404


from user.forms import SignUpForm, SignInForm
from user.models import Profile

def signUp(request):
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
    return render(request, 'signup.html', context)

def signIn(request):
    if request.method == 'GET':
        form = SignInForm()
    elif request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['Login'], 
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
    return render(request, 'signin.html', context)

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
        'student': student
    }
    return render(request, 'student_profile.html', context)
