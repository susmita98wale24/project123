from django.contrib import admin
from .models import Book, Rating
from import_export.admin import ExportMixin
from .resource import BookResource, RatingResource


@admin.register(Book)
class BookAdmin(ExportMixin, admin.ModelAdmin):
    # Display these fields in the admin list view
    resource_class = BookResource
    list_display = ('book_name', 'author', 'category', 'publication_year', 'isbn', 'title', 'id', 'purchase_link')
    
    # Add search functionality for these fields
    search_fields = ('book_name', 'author', 'category', 'isbn', 'title')
    
    # Add filters for quick access to certain categories
    list_filter = ('category', 'publication_year')
    
    # Make fields editable directly from the list view
    list_editable = ('category', 'publication_year')
    
    # Customize how the records are ordered
    ordering = ('-publication_year', 'book_name', 'title', 'id')
    
    # Limit the number of items displayed per page
    list_per_page = 20
    
    # Group fields logically in the detailed view
    fieldsets = (
        ('Book Details', {
            'fields': ('book_name', 'author', 'category', 'description', 'title', 'purchase_link')
        }),
        ('Publication Info', {
            'fields': ('publication_year', 'isbn')
        }),
        ("Media", {
            'fields': ("image",)
        }),
    )

    # Add date hierarchy for easier navigation
    date_hierarchy = 'publication_year'

class RatingAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = RatingResource


admin.site.register(Rating, RatingAdmin)