from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'Customer'

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    author = models.CharField(max_length=100,null=True)
    price = models.FloatField()
    Category = models.CharField(max_length=100,null=True)
    stock = models.BooleanField(default=False, null=True, blank=False)
    image= models.ImageField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'Product'
        ordering = ['-created']

class Order(models.Model):
    customer = models.ForeignKey(Customer,blank=True, null=True,on_delete=models.SET_NULL)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True)
    transaction_id = models.CharField(max_length=200,null=True)
    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    class Meta:
        db_table = 'Order'
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, null=True,on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True,on_delete=models.SET_NULL)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address
    class Meta:
        db_table = 'ShippingAddress'


class OrderItem(models.Model):
    product = models.ForeignKey(Product,blank=True,null=True,on_delete=models.SET_NULL)
    Order = models.ForeignKey(Order, blank=True, null=True,on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0,blank=True,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'OrderItem'
    @property
    def get_total(self):
        total=self.product.price * self.quantity
        return total

