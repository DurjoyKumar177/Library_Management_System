from django.views.generic import ListView, DetailView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import Book, Borrow, Category
from transactions.models import Transaction
from transactions.constants import PAYMENT


# List all books
class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'  
    context_object_name = 'books'

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            # If a category slug is passed, filter books by category
            category = get_object_or_404(Category, slug=category_slug)
            return Book.objects.filter(catagory=category)
        else:
            # If no category slug is provided, return all books
            return Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Pass all categories to the template
        return context



# Display details of a specific book
class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_details.html'  # Updated the template name to match conventions
    context_object_name = 'book'

    def get_object(self):
        # Fetch the book using the primary key from the URL
        return get_object_or_404(Book, pk=self.kwargs['pk'])


# Show borrow history of the logged-in user
@method_decorator(login_required, name='dispatch')
class BorrowHistoryView(ListView):
    model = Borrow
    template_name = 'profile.html'  
    context_object_name = 'borrows'

    def get_queryset(self):
        # Fetch borrow history only for the logged-in user
        return Borrow.objects.filter(user=self.request.user)


# Borrow a book if available
@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user_account = request.user.account  
    
    # Check if the user has enough balance
    if user_account.balance >= book.borrowprice:
        if book.quantity > 0:
            # Deduct the borrow price from the user's balance
            user_account.balance -= book.borrowprice
            user_account.save()

            # Record the payment transaction
            Transaction.objects.create(
                account=user_account,
                amount=book.borrowprice,
                balance_after_transaction=user_account.balance,
                transaction_type=PAYMENT,
            )

            # Reduce the book's quantity
            book.quantity -= 1
            book.save()

            # Create a Borrow record
            Borrow.objects.create(user=request.user, book=book)

            # Show success message and redirect to profile
            messages.success(request, f"You have successfully borrowed '{book.title}'.")
            return redirect('profile')
        else:
            # Book is out of stock
            messages.error(request, f"'{book.title}' is currently unavailable.")
    else:
        # User doesn't have enough balance
        messages.error(request, "Insufficient balance to borrow this book.")

    return redirect('book_list')