from django.urls import path
from .views import BookListView, BookDetailView, BorrowHistoryView, borrow_book

urlpatterns = [
    path('book_list', BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_details'),
    path('borrow/<int:book_id>/', borrow_book, name='borrow_book'),
    path('book_history/', BorrowHistoryView.as_view(), name='book_history'),
    path('category/<slug:category_slug>/', BookListView.as_view(), name='book_list_by_category'),
]
