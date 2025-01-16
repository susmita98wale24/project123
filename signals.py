from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Book, Review

# Signal to perform an action when a new user is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print(f"Profile created for user: {instance.username}")

# Signal to modify a book's data before saving
@receiver(pre_save, sender=Book)
def update_book_info(sender, instance, **kwargs):
    # Example: Capitalize the book title before saving
    instance.title = instance.title.title()
    print(f"Book info updated for: {instance.title}")

# Signal to perform an action when a review is deleted
@receiver(post_delete, sender=Review)
def delete_review(sender, instance, **kwargs):
    print(f"Review deleted for book: {instance.book.title}")