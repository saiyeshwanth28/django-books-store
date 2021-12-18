from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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
    return render(request,'register.html',context)
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return render(request,'store.html')
        else:
            messages.info(request,'Username or password is incorrect')
    context={}
    return render(request,'login.html',context)

def store(request):
    products = Product.objects.all()
    page = request.GET.get('page')
    results = 6
    paginator = Paginator(products, results)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        page = 1
    except EmptyPage:
        page=paginator.num_pages
    context = {'products': products,'paginator': paginator}
    return render(request,'store.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items=[]
    context = {'items': items,'order':order}
    return render(request,'cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items=[]
    context = {'items': items,'order':order}
    return render(request,'checkout.html',context)

def search(request):
    search_query=''
    if request.GET.get('search_query'):
        search_query= request.GET.get('search_query')
    print(search_query)
    results = Product.objects.filter(name__icontains=search_query)
    return render(request,'search.html',{'results':results})
