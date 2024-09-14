from django.db import models
from accounts.models import User



class Books(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    author = models.CharField(max_length=255, null=False, blank=False)
    genre = models.CharField(max_length=100)
    number_of_copies = models.IntegerField() 
    isbn = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return f"{self.author}:{self.title}"


class BookRequest(models.Model):
    PENDING = 'PENDING'
    CANCEL = 'CANCEL'
    APPROVE = 'APPROVE'

    BOOK_REQUEST_CHOICES = [
        (PENDING, 'Pending'),
        (CANCEL, 'Cancel'),
        (APPROVE, 'Approve')
    ]

    library_user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="book_requests")
    book = models.ForeignKey(Books, on_delete=models.RESTRICT, related_name="books")
    book_request_status = models.CharField(default=PENDING, max_length=15, choices=BOOK_REQUEST_CHOICES)
    
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.library_user.email}: {self.book.title} {self.book.isbn}"
