from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import Book, Borrow, Category, Review
from transactions.models import Transaction
from transactions.constants import PAYMENT, REFUND
from .forms import ReviewForm
from django.utils.timezone import now
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_transaction_email(user_account, book, subject, template):
    user = user_account  # Assuming the passed object is a User object
    message = render_to_string(template, {
        'user': user,
        'book': book,
        'amount': book.borrowprice,  # Ensure the borrow price is passed
        'title': book.title,         # Add the book title to the context
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


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
    template_name = 'books/book_details.html'
    context_object_name = 'book'

    def get_object(self):
        # Fetch the book using the primary key from the URL
        return get_object_or_404(Book, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        # Extend context with reviews and borrowed status
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context['reviews'] = Review.objects.filter(book=book).order_by('-id')  # Fetch and order reviews

        # Check if the user is authenticated before querying Borrow
        if self.request.user.is_authenticated:
            # Only show borrowed status for authenticated users
            context['user_has_borrowed'] = Borrow.objects.filter(
                user=self.request.user, book=book, returned=False
            ).exists()
        else:
            # Set borrowed status to False for unauthenticated users
            context['user_has_borrowed'] = False
        
        return context


# Show borrow history of the logged-in user
@method_decorator(login_required, name='dispatch')
class BorrowHistoryView(ListView):
    model = Borrow
    template_name = 'books/profile.html'
    context_object_name = 'borrows'

    def get_queryset(self):
        # Fetch borrow history only for the logged-in user, ordered by the most recent borrow_date
        return Borrow.objects.filter(user=self.request.user).order_by('-borrow_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the current datetime for use with the `timesince` filter
        context['current_time'] = now()
        return context


# Borrow a book if available
@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user_account = request.user.account

    # Check if the user has already borrowed this book and hasn't returned it
    if Borrow.objects.filter(user=request.user, book=book, returned=False).exists():
        messages.error(request, f"You have already borrowed '{book.title}'. Check your 'My Books' for details.")
        return redirect('book_list')

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
            send_transaction_email(request.user, book, 'Book Borrow Confirmation', 'books/book_borrow_email.html')
            return redirect('profile')
        else:
            # Book is out of stock
            messages.error(request, f"'{book.title}' is currently unavailable.")
    else:
        # User doesn't have enough balance
        messages.error(request, "Insufficient balance to borrow this book.")

    return redirect('book_list')


@login_required
def return_book(request, book_id):
    borrow = get_object_or_404(Borrow, user=request.user, book_id=book_id, returned=False)
    account = request.user.account

    # Update the borrow record
    borrow.returned = True
    borrow.save()

    # Increment the book quantity
    book = borrow.book
    book.quantity += 1
    book.save()

    # Refund the book price to the user's account
    refund_amount = borrow.book.borrowprice
    account.balance += refund_amount
    account.save(update_fields=['balance'])

    # Record the refund transaction
    Transaction.objects.create(
        account=account,
        amount=refund_amount,
        balance_after_transaction=account.balance,
        transaction_type=REFUND
    )

    # Display a success message
    messages.success(
        request,
        f'{refund_amount:.2f} $ was refunded to your account successfully.'
    )

    send_transaction_email(request.user, borrow.book, 'Book Return Confirmation', 'books/book_return_email.html')

    return redirect('profile')


@login_required
def review_book(request, book_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book_id = book_id
            review.save()
            return redirect('profile')
    else:
        form = ReviewForm()
    return render(request, 'books/review_book.html', {'form': form})

class MyBookView(LoginRequiredMixin, ListView):
    model = Borrow
    template_name = 'books/borrowed_book.html'
    context_object_name = 'borrows'

    def get_queryset(self):
        # Fetch only the books borrowed by the logged-in user
        return Borrow.objects.filter(user=self.request.user, returned=False).order_by('-borrow_date')