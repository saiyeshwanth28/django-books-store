from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
import json
from django.core.paginator import Paginator
# Create your views here.
def home(request):
    return render(request,"main.html")

"""def registerPage(request):
    if request.method=="POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        users = Customer.objects.all()
        if password1 == password2:
            user = Customer(username=username,email=email,password=password1)
            user.save()
            messages.success(request,"Account created successfully")
            return render(request,'login.html')
        else:
            return HttpResponse("passwords did'nt match")
    return render(request,'register.html')

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        users = Customer.objects.all()
        for user in users:
            if user.username == username and user.password== password:
                return redirect('store')
    return render(request,'login.html')"""

def logout(request):
    return redirect('login')

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
        products = Product.objects.all()
        page = request.GET.get('page')
        results = 6
        paginator = Paginator(products, results)
        context = {'products': products,'paginator': paginator,'cartItems': cartItems}
        return render(request,'store.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        print(cartItems)
    else:
        items=[]
    context = {'items': items,'order':order,'cartItems': cartItems}
    return render(request,'cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items=[]
    context = {'items': items,'order':order,'cartItems': cartItems}
    return render(request,'checkout.html',context)

def search(request):
    search_query=''
    if request.GET.get('search_query'):
        search_query= request.GET.get('search_query')
    print(search_query)
    results = Product.objects.filter(name__icontains=search_query)
    return render(request,'search.html',{'results':results})

def category(request):
    category= request.GET.get('menu')
    results = Product.objects.filter(Category__icontains=category)
    return render(request,'search.html',{'results':results})

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(Order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def detail(request,id):
    product_object = Product.objects.get(id=id)
    return render(request,'details.html',{'product_object':product_object})


def registerPage(request):
    form = CreateUserForm()
    if request.method=="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context={'form':form}
    if request.user.is_authenticated:
        return redirect('store')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        context = {'form': form}
        return render(request,'register.html',context)
    return render(request,'register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('store')
        context = {}
        return render(request, 'login.html',context)
