from django.urls import path
from django.contrib import admin
from .views import BooksListView, BooksDetailView, BookCheckoutView, paymentComplete, SearchResultsListView, book_detail, AddToCar, ViewCart, RemoveItem, CheckOut, checkoutResult, RemoveAll

urlpatterns = [
    path('', BooksListView.as_view(), name = 'list'),
    path('<int:pk>/',book_detail, name = 'detail'),
    path('<int:pk>/checkout/', BookCheckoutView.as_view(), name = 'checkout'),
    # path('checkout/', BookCheckoutView.as_view(), name = 'checkout'),
    path('complete/', paymentComplete, name = 'complete'),
    path('search/', SearchResultsListView.as_view(), name = 'search_results'),
    path('add_to_cart/', AddToCar, name='add_to_cart'),
    path('cart/', ViewCart, name='cart'),
    path('remove_item_from_cart/', RemoveItem, name='remove_item_from_cart'),
    path('remove_all/', RemoveAll,name='remove_all'),
    path('check_out/', CheckOut, name='check_out'),
    path('checkout_result/<str:email>/', checkoutResult, name='checkout_result'),

    path('admin', admin.site.urls)
]