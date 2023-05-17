from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from audioop import avg, avgpp
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book, Order,OrderDetail
from django.contrib.auth.mixins import LoginRequiredMixin 
from .models import Book, Order, Review, Category
from .models import Book, Order, OrderDetail, Review, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q  # for search method
from django.http import JsonResponse
import json
from django.db.models import Avg
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required


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
    return render(request, 'checkout_result.html', {'email': email})


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
    rating_value = Review.objects.filter(
        book=book).aggregate(avg=Avg('rating'))['avg']
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


def get_all_categories(request):
    categories = Category.objects.all()
    books = Book.objects.all()
    #convert books.price to int
    for book in books:
        book.price = int(book.price)

    category_query = request.GET.get('category')
    if category_query:
        books = Book.objects.filter(category__name=category_query)

    for book in books:
        rating_value = Review.objects.filter(book=book).aggregate(avg=Avg('rating'))['avg']
        if rating_value == None:
            rating_value = 0
        else:
            rating_value = round(rating_value, 1)
        book.rating_value = rating_value
        
    if request.method == 'POST':
        ca = request.POST.getlist('category')
        if ca:
            if 'all' in ca:
                books = Book.objects.all()
                
            else:
            # filter books by category
                books = Book.objects.filter(category__in=ca)
        else:
            books = Book.objects.all()
            
        for book in books:
           book.price = int(book.price)
           rating_value = Review.objects.filter(book=book).aggregate(avg=Avg('rating'))['avg']
           if rating_value == None:
                rating_value = 0
           else:
                rating_value = round(rating_value, 1)
           book.rating_value = rating_value

    return render(request, 'list.html', {'categories': categories,
                                         'books': books})

def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    book.price = int(book.price)
    rating_value = Review.objects.filter(
        book=book).aggregate(avg=Avg('rating'))['avg']
    if rating_value == None:
        rating_value = 0
    else:
        rating_value = round(rating_value, 1)
    num_of_reviews = Review.objects.filter(book=book).count()
    reviews = Review.objects.filter(book=book)
    context = {
        "book": book,
        "rating_value": rating_value,
        "num_of_reviews": num_of_reviews,
        "reviews": reviews,
    }

    return render(request, "detail.html", context)


@csrf_exempt
def AddToCart(request):
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
                'cover': str(book.cover),
                'price': book.price,
                'quantity': quantity,
                'subtotal': quantity*book.price
            }
        request.session['cart_subtotal'] += quantity*book.price
    request.session.modified = True
    return JsonResponse('Add completed!', safe=False)

@csrf_exempt
def sendReview(request):
    body = json.loads(request.body)
    Review.objects.create(review=body['review'],
                          rating=body['rating'],
                          created_at=body['created_at'],
                          book_id=body['book_id'],
                          user_id=body['user_id'])
    return JsonResponse('Add completed!', safe=False)

def ViewCart(request):
    cart = request.session.get('cart', {})
    subtotal = request.session.get('cart_subtotal') or 0
    code = request.session.get('code')
    return render(request, 'cart.html', {'cart': cart, 'cart_subtotal': subtotal, 'code': code})


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

@login_required(login_url='/login') 
def getAllOdersByUser(request):
    listorder = []
    userid = request.user.id
    orders = Order.objects.filter(user=userid)
    for order in orders:
        listorder.append({
            'order':order,
            'listdetail':OrderDetail.objects.filter(order=order)
        })
    context = {'listorder': listorder}

    return render(request, "purchase_history.html", context)

@csrf_exempt
def CheckOut(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        body = json.loads(request.body)
        email = body.get('email')
        total = 0
        for productID, product in cart.items():
            total += int(product['subtotal'])
        order = Order.objects.create(email=email, total_price=total, user_id=request.user.id)
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

 

@csrf_exempt
def send_verification_code(request):
    # request.session.get['code']= ""
    if request.method == 'POST':
        body = json.loads(request.body)
        email = body.get('email')
    # Tạo mã xác nhận ngẫu nhiên
        verification_code = get_random_string(length=6)
        # Gửi email
        subject = 'Mã xác nhận'
        message = f'Mã xác nhận của bạn là: {verification_code}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
        if 'cart' not in request.session:
            request.session['code'] = {}
            request.session['code'] = verification_code
        else:
            request.session['code'] = verification_code
    print(request.session['code'])
    return JsonResponse('Email sent!', safe=False)


@csrf_exempt
def Confirm(request):
    print(request.session.get('code'))
    if request.method == 'POST':
        user_input_code = request.POST.get('user_input')  
        code_verification = request.session.get('code')
        print(user_input_code, code_verification)
        if code_verification == user_input_code:
            message = 'Code verification'
            print(message)
            return render(request, 'cart.html', {'message':message})
        else:
            message = 'Code not verification'
            print(message)
            return render(request, 'cart.html', {'message': message})
