from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.conf import settings

class Book(models.Model):
    title = models.CharField(max_length=255, default="Unknown")  # Book title
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)  # Average rating
    book_name = models.CharField(max_length=250)
    author = models.CharField(max_length=150, default="Unknown", blank=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    publication_year = models.DateField(default=date.today, blank=True, null=True)
    isbn = models.CharField(max_length=13, blank=True, null=True)
    pdf = models.FileField(upload_to="books/pdfs/", blank=True, null=True)
    purchase_link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to="books/images/", blank=True, null=True, default="books/images/default.jpg")
    description = models.TextField(blank=True, null=True)  # Optional description for the book

    def save(self, *args, **kwargs):
        if self.publication_year and not isinstance(self.publication_year, str):
            self.publication_year = self.publication_year.strftime('%Y-%m-%d')
            super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def _str_(self):
        return self.book_name

    @property
    def average_rating(self):
        """
        Calculate the average rating for the book.
        """
        ratings = self.ratings.all()
        return sum(r.rating for r in ratings) / len(ratings) if ratings else None

    @property
    def total_reviews(self):
        """
        Get the total number of reviews for the book.
        """
        return self.ratings.count()

    def get_top_reviews(self, count=3):
        """
        Retrieve the top reviews based on the rating.
        """
        return self.ratings.order_by('-rating')[:count]


class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, f"{i} Stars") for i in range(1, 6)])
    review = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('book', 'user')  # Ensure one user can review a book only once

    def _str_(self):
        return f"{self.book.book_name} - {self.rating} Stars by {self.user.username}"


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, f"{i} Stars") for i in range(1, 6)])
    review = models.TextField()

    def _str_(self):
        return f"Review for {self.book.book_name} by {self.user.username}"

    def is_positive(self):
        """
        Check if the review is positive (4 or 5 stars).
        """
        return self.rating >= 4
    
class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="search_histories")
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.username}: {self.query} at {self.timestamp}"