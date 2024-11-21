from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)    
    def __str__(self):
        return self.name
class Book(models.Model):
        title = models.CharField(max_length=100)
        description = models.TextField()
        borrowprice = models.DecimalField(max_digits=10, decimal_places=2)
        quantity = models.IntegerField(default=1)
        image = models.ImageField(upload_to='books/uploads/', null=True, blank=True)
        catagory = models.ForeignKey(Category, on_delete=models.CASCADE)       

        def __str__(self):
            return self.title

class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating 1-5
    comment = models.TextField()

    def __str__(self):
        return f"Review by {self.user.username} on {self.book.title}"
