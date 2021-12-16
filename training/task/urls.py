from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.store,name="store"),
    path('register/',views.registerPage,name="register"),
    path('login/',views.loginPage,name="login"),
    path('cart/',views.cart,name="cart"),
    path('checkout/', views.checkout, name="checkout"),
]
