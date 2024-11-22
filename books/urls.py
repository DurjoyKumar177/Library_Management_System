from django.urls import path
from .views import BookListView, BookDetailView, BorrowHistoryView,MyBookView, borrow_book, return_book, review_book

urlpatterns = [
    path('book_list', BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_details'),
    path('borrow/<int:book_id>/', borrow_book, name='borrow_book'),
    path('book_history/', BorrowHistoryView.as_view(), name='profile'),
    path('category/<slug:category_slug>/', BookListView.as_view(), name='book_list_by_category'),
    path('return/<int:book_id>/', return_book, name='return_book'),
    path('review/<int:book_id>/', review_book, name='review_book'),
    path('my_books/', MyBookView.as_view(), name='my_books'),
]
