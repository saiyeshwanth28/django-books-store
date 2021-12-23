from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.store,name="store"),
    path('register/',views.registerPage,name="register"),
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logout,name="logout"),
    path('search/',views.search,name="search"),
    path('category/',views.category,name="category"),
    path('cart/',views.cart,name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('updateItem/', views.updateItem, name="updateItem"),
    path('<int:id>/', views.detail,name="details")
]
