from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile


# Create your views here.


@login_required(login_url='signin')
def index(request):
    return render(request,'index.html')

def signup(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        co_password=request.POST['co_password']

        if password == co_password:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email is already signed up')
                return redirect('signup')
            
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username is already taken')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,password=password,email=email)
                user.save()

                #log user in and redirect to settings.html
                user_login=auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
                #create profile object of the user

                user_model=User.objects.get(username=username)
                new_profile=Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect('signup')
        else:
            messages.info(request,'Your Passwords are not matching.')
            return redirect('signup')


    else:
        return render(request, 'signup.html')
    
def signin(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        
        else:
            messages.info(request,'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request,'signin.html')  
    
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin.html')

@login_required(login_url='signin')
def settings(request):
    return render(request, 'settings.html')