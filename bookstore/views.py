from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Author, Category, Review

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def getAllBooks(request, category_id, author_id, rating, price):

    books = Book.objects.all()
    context = { 
        'books': books
    }
    return render(request, 'bookstore/index.html',)
