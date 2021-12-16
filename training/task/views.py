from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.
def home(request):
    context={}
    return render(request,"main.html",context)
def search(request):
    return HttpResponse("Search for the content")
def registerPage(request):
    form = CreateUserForm()
    if request.method=="POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account created successfully")
            return redirect('login')
    context={'form':form}
    return render(request,"register.html",context)
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return render(request,"main.html")
        else:
            messages.info(request,'Username or password is incorrect')
    context={}
    return render(request,"login.html",context)

def store(request):
    context = {}
    return render(request,'store.html',context)

def cart(request):
    context = {}
    return render(request,'cart.html',context)

def checkout(request):
    context = {}
    return render(request,'checkout.html',context)