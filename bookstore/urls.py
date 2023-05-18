from .views import BooksListView, BooksDetailView, SearchResultsListView, paymentComplete, book_detail, AddToCart, ViewCart, RemoveItem, CheckOut, checkoutResult, RemoveAll, home, send_verification_code, Confirm, getAllOdersByUser, get_all_categories, sendReview
from django.urls import path

urlpatterns = [
    #pages
    path('', home, name = 'home'),
    path('list', get_all_categories, name = 'list'),
    path('<int:pk>',book_detail, name = 'detail'),
    path('cart/', ViewCart, name='cart'),
    path('purchase-history/', getAllOdersByUser, name='purchase-history'),
    path('checkout_result/<str:email>/', checkoutResult, name='checkout_result'),

    #api endpoints
    path('search/', SearchResultsListView.as_view(), name = 'search_results'),
    path('complete/', paymentComplete, name = 'complete'),
    path('add_to_cart/', AddToCart, name='add_to_cart'),
    path('send_review/', sendReview, name='send_review'),
    path('remove_item/<str:item_id>/', RemoveItem, name='remove_item'),
    path('remove_all/', RemoveAll,name='remove_all'),
    path('check_out/', CheckOut, name='check_out'),
    path('send_verification/', send_verification_code, name='send_verification'),
    path('confirm/', Confirm, name='confirm'),
]