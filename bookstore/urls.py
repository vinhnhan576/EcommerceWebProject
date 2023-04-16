from django.urls import path
from .views import BooksListView, BooksDetailView, BookCheckoutView, paymentComplete, SearchResultsListView, AddToCar, ViewCart, RemoveItem, CheckOut, RemoveAll

urlpatterns = [
    path('', BooksListView.as_view(), name = 'list'),
    path('<int:pk>/', BooksDetailView.as_view(), name = 'detail'),
    path('checkout/', BookCheckoutView.as_view(), name = 'checkout'),
    path('complete/', paymentComplete, name = 'complete'),
    path('search/', SearchResultsListView.as_view(), name = 'search_results'),
    path('add_to_cart/', AddToCar, name='add_to_cart'),
    path('view_cart/', ViewCart, name='view_cart'),
    path('remove_item_from_cart/', RemoveItem, name='remove_item_from_cart'),
    path('remove_all/', RemoveAll,name='remove_all'),
    path('check_out/', CheckOut, name='check_out'),
]