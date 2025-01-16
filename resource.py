from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Book, Rating

class BookResource(resources.ModelResource):
    # Customizing fields for export and import
    author_name = fields.Field(
        column_name='author_name',
        attribute='author',
        widget=ForeignKeyWidget(Book, 'id')
    )

    class Meta:
        model = Book
        fields = [
            'id', 'book_name', 'author', 'category', 'isbn',
            'publication_year', 'purchase_link', 'created_date'
        ]
        export_order = [
            'id', 'book_name', 'author', 'category',
            'isbn', 'publication_year', 'purchase_link', 'created_date'
        ]
        import_id_fields = ['id']
        skip_unchanged = True
        report_skipped = True

    def before_import_row(self, row, **kwargs):
        """
        Hook to process data before importing each row.
        """
        # Example: Auto-fill missing data
        if not row.get('author'):
            row['author'] = "Unknown Author"

    def after_import_instance(self, instance, new, **kwargs):
        """
        Hook to perform actions after importing a row.
        """
        if new:
            print(f"New book added: {instance.book_name}")
        else:
            print(f"Updated book: {instance.book_name}")


class RatingResource(resources.ModelResource):
    user_name = fields.Field(
        column_name='user_name',
        attribute='user',
        widget=ForeignKeyWidget(Rating, 'id')
    )
    book_name = fields.Field(
        column_name='book_name',
        attribute='book',
        widget=ForeignKeyWidget(Rating, 'id')
    )

    class Meta:
        model = Rating
        fields = [
            'id', 'book', 'user', 'rating', 'review'
        ]
        export_order = [
            'id', 'book_name', 'user_name', 'rating', 'review'
        ]
        import_id_fields = ['id']
        skip_unchanged = True
        report_skipped = True

    def before_import_row(self, row, **kwargs):
        """
        Hook to process data before importing each row.
        """
        # Ensure the rating is within a valid range
        if not (1 <= int(row['rating']) <= 5):
            row['rating'] = 3  # Set default rating if invalid

    def after_import_instance(self, instance, new, **kwargs):
        """
        Hook to perform actions after importing a row.
        """
        if new:
            print(f"New rating added for book: {instance.book.book_name}")
        else:
            print(f"Updated rating for book: {instance.book.book_name}")