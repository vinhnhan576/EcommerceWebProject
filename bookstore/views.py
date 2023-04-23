from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from audioop import avg, avgpp
from django.shortcuts import render 
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book, Order, OrderDetail, Review, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q  # for search method
from django.http import JsonResponse
import json
from django.db.models import Avg


class BooksListView(ListView):
    model = Book
    template_name = 'list.html'


class BooksDetailView(DetailView):
    model = Book
    template_name = 'detail.html'


class SearchResultsListView(ListView):
    model = Book
    template_name = 'search_results.html'

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        return Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )

class BookCheckoutView(ListView):
    model = Book
    template_name = 'checkout.html'
    # login_url     = 'login'
    # login_url = 'login'

    # def checkout(request):
    #     if request.method == 'POST':
    #         body = json.loads(request.body)
    #         product_id = body.get('productId')
    #         if not product_id:
    #             return JsonResponse({'error': 'productId is required'}, status=400)
    #         try:
    #             product = Book.objects.get(id=product_id)
    #         except Book.DoesNotExist:
    #             return JsonResponse({'error': 'Invalid productId'}, status=400)
    #         order = Order.objects.create(
    #             user=request.user,
    #             product=product
    #         )
    #         return JsonResponse({'orderId': order.id})
    #     else:
    #         return JsonResponse({'error': 'Invalid request method'}, status=400)

from django.db.models import Sum
def home(request):
    book_num = 5
    category_num = 4
    books = Book.objects.order_by('-sold_quantity')[:book_num]
    top_books = []
    for book in books:
        rating_value = Review.objects.filter(book=book).aggregate(avg=Avg('rating'))['avg']
        top_books.append({'book': book, 'rating': rating_value})
    
    categories = Category.objects.annotate(sold_quantity=Sum("book__sold_quantity")).order_by("-sold_quantity")[:category_num]
    top_categories = []
    for category in categories:
        print(category.__getattribute__('sold_quantity'))
        top_categories.append({'category_info' : category, 'books' : Book.objects.filter(category=category).order_by("-sold_quantity")[:book_num]}) 

    return render(request, 'home.html', {"top_books": top_books, "top_categories": top_categories})

def checkoutResult(request, email):
    return render(request, 'checkout_result.html', {'email' : email})

def paymentComplete(request):
    body = json.loads(request.body)
    print('BODY:', body)
    product = Book.objects.get(id=body['productId'])
    Order.objects.create(
        product=product
    )
    return JsonResponse('Payment completed!', safe=False)

def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    rating_value = Review.objects.filter(book=book).aggregate(avg=Avg('rating'))['avg']
    num_of_reviews = Review.objects.filter(book=book).count()    
    # form = CommentForm()
    # if request.method == 'POST':
    #     form = CommentForm(request.POST)
    #     if form.is_valid():
    #         comment = Comment(
    #             author=form.cleaned_data["author"],
    #             body=form.cleaned_data["body"],
    #             post=post
    #         )
    #         comment.save()
    # comments = Comment.objects.filter(post=post)
    context = {
        "book": book,
        "rating_value": rating_value,
        "num_of_reviews": num_of_reviews
    }   

    return render(request, "detail.html", context)

def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    rating_value = Review.objects.filter(book=book).aggregate(avg=Avg('rating'))['avg']
    num_of_reviews = Review.objects.filter(book=book).count()  
    reviews = Review.objects.filter(book=book)
    context = {
        "book": book,
        "rating_value": rating_value,
        "num_of_reviews": num_of_reviews,
        "reviews": reviews
    }   

    return render(request, "detail.html", context)

@csrf_exempt
def AddToCar(request):
    if 'cart' not in request.session:
        request.session['cart'] = {}
    if 'cart_subtotal' not in request.session:
        request.session['cart_subtotal'] = 0
    if request.method == 'POST':
        body = json.loads(request.body)
        bookId = body['id']
        quantity = int(body['quantity'])
        book = Book.objects.get(id=bookId)
        if bookId in request.session['cart']:
            request.session['cart'][bookId]['quantity'] += quantity
            request.session['cart'][bookId]['subtotal'] += request.session['cart'][bookId]['quantity']*book.price
        else:
            request.session['cart'][bookId] = {
                'name': book.title,
                'author': book.author.name,
                'cover': book.cover,
                'price': book.price,
                'quantity': quantity,
                'subtotal':quantity*book.price
            }
        request.session['cart_subtotal'] += quantity*book.price
    request.session.modified = True
    return JsonResponse('Add completed!', safe=False)

def ViewCart(request):
    cart = request.session.get('cart', {})
    subtotal = request.session.get('cart_subtotal')
    return render(request, 'cart.html', {'cart': cart, 'cart_subtotal': subtotal})
    

def RemoveItem(request, item_id):
    cart = request.session.get('cart', {})
    if item_id in cart:
        del cart[item_id]
    request.session['cart'] = cart
    return JsonResponse('Remove completed!', safe=False)

def RemoveAll(request):
    cart = request.session.get('cart', {})
    cart.clear()
    request.session['cart'] = cart
    request.session['cart_subtotal'] = 0
    return JsonResponse('Remove completed!', safe=False)

@csrf_exempt
def CheckOut(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        body = json.loads(request.body)
        email = body.get('email')
        total = 0
        for productID, product in cart.items():
            total += int(product['subtotal'])
        order = Order.objects.create(email=email, total_price=total)
        for productID, product in cart.items():
            product1 = Book.objects.get(pk=productID)
            print("before", product1.quantity)
            quantity = int(product.get('quantity'))
            order_detail = order.detail.through.objects.create(
                order=order, book=product1, quantity=quantity, total_price=product['subtotal'])
            order_detail.save()
            product2 = Book.objects.get(pk=productID)
            product2.sold_quantity += quantity
            product2.quantity -= quantity
            product2.save()
            print("after", product2.quantity)
        RemoveAll(request)
        print('success')
    return JsonResponse('Checkout completed!', safe=False)

def error404View(request, exception):
    return render(request, '404.html')