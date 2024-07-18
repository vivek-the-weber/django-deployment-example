from django.shortcuts import render
from basic_app.models import UserProfileInfo
from basic_app.forms import UserForm,UserProfileInfoForm
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')
def register(request):
    registered=False

    if request.method=="POST":
        user_form = UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user=user_form.save()#save the user input information into the database
            user.set_password(user.password)#set_password() method grabs the password from the database and hashes the password
            user.save()#saves the changes made after any performed operations on the data here hashed password in the database

            profile=profile_form.save(commit=False)
            profile.user=user

            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']

            profile.save()
            registered=True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()

    return render(request,'basic_app/registration.html',{
        'user_form':user_form,
        'profile_form':profile_form,
        'registered':registered,
    })


def user_login(request):

    if request.method=="POST":
        username=request.POST.get('username')#name="username"
        password=request.POST.get('password')#name="password"

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed")
            print(f"Username {username}\nPassword {password}")
            return HttpResponse("Invalid Login Details Supplied")
    else:
        return render(request,'basic_app/login.html',{})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse("You are logged in!")