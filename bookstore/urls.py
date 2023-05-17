from .views import BooksListView, BooksDetailView, BookCheckoutView, paymentComplete, SearchResultsListView, book_detail, AddToCart, ViewCart, RemoveItem, CheckOut, checkoutResult, RemoveAll, home, send_verification_code, Confirm, getAllOdersByUser, get_all_categories, sendReview
from django.urls import path

urlpatterns = [
    path('', home, name = 'home'),
    path('list', get_all_categories, name = 'list'),
    path('<int:pk>/',book_detail, name = 'detail'),
    path('<int:pk>/checkout/', BookCheckoutView.as_view(), name = 'checkout'),
    path('complete/', paymentComplete, name = 'complete'),
    path('search/', SearchResultsListView.as_view(), name = 'search_results'),
    path('add_to_cart/', AddToCart, name='add_to_cart'),
    path('send_review/', sendReview, name='send_review'),
    path('cart/', ViewCart, name='cart'),
    path('remove_item_from_cart/', RemoveItem, name='remove_item_from_cart'),
    path('remove_all/', RemoveAll,name='remove_all'),
    path('check_out/', CheckOut, name='check_out'),
    path('checkout_result/<str:email>/', checkoutResult, name='checkout_result'),
    path('send_verification/', send_verification_code, name='send_verification'),
    path('confirm/', Confirm, name='confirm'),
    path('purchase-history/', getAllOdersByUser, name='purchase-history'),
]