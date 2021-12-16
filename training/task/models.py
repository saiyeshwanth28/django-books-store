from django.db import models

# Create your models here.
class book_details(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    price = models.FloatField()
    category= models.CharField(max_length=100)
    class Meta:
        db_table = 'Book_details'