from django.db import models
from EcommerceWebProject.settings import AUTH_USER_MODEL
from django.contrib.auth import get_user_model


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=500, default=None)
    cover = models.ImageField(upload_to='static/images/books/covers', default=None)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    price = models.FloatField(null=True, blank=True)
    published_date = models.DateField()
    quantity = models.IntegerField()
    sold_quantity = models.IntegerField()
    book_available = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.name


# class User(models.Model):
#     username = models.CharField(max_length=50, unique=True)
#     password = models.CharField(max_length=50)
#     address = models.CharField(max_length=1000, default="Hanoi")
#     phone = models.CharField(max_length=1000, default="0123456789")

#     def __str__(self):
#         return self.user.username


class Review(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.review


class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=1000)
    detail = models.ManyToManyField(Book, through='OrderDetail')
    total_price = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order


class OrderDetail(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField(default=100)

    def __str__(self):
        return self.orderdetail
