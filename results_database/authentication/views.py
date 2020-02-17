from django.shortcuts import render,redirect,HttpResponse
from .form import *
from django.contrib.auth import authenticate, login, logout
from .auth_backend import AuthBackend
from submission.models import *
from .models import *


# Create your views here.
def loginto(request):
    if request.method == 'POST':
        form = login_form(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user_auth = authenticate(name = cd['name'], password = cd['password'], institution_name = cd['institution_name'])

            if user_auth is not None:
                if user_auth.is_active:
                    login(request, user_auth)
                    return redirect('/load_dashboard')
                else:
                    return HttpResponse('User disabled')
            else:
                return HttpResponse("User is not valid")
        else:
            form = login_form()
            return HttpResponse("Enter form correctly")
    else:
        form = login_form()
    return render(request, 'login.html', {'form':form})

def signup(request):
    if request.method == "POST":

        form = signup_form(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            Users.objects.create_user(cd["user_name"],cd["email"],cd["institution_name"],cd["password"])

            return redirect("load_dashboard")

    else:
        form = signup_form()

    return render(request,"signup.html",{"form":form})

def create_institution(request):
    if request.method == "POST":

        form = institution_form(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            Institution.objects.create_institution(cd["institution_name"],cd["address"],cd["website"],cd["telephone"])

            return redirect("/login")

    else:
        form = institution_form()

    return render(request,"institution.html",{"form":form})

def logout(request):
    logout('request')
    return redirect('/login')
