from django import forms
from .models import Book, Rating

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'book_name', 'title', 'author', 'category',
            'publication_year', 'isbn', 'pdf', 'purchase_link'
        ]
        widgets = {
            'book_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book name',
                'style': 'border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Author name',
                'style': 'border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
                'style': 'border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Year of publication',
                'style': 'border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ISBN number',
                'style': 'border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'
            }),
            'pdf': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'style': 'border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'
            }),
            'purchase_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Purchase link',
                'style': 'border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'
            }),
            'title': forms.TextInput(attrs={  # Title widget
                'class': 'form-control',
                'placeholder': 'Enter book title',
                'style': 'border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);',
            }),
        }
        labels = {
            'book_name': 'Book Name',
            'author': 'Author',
            'category': 'Category',
            'publication_year': 'Publication Year',
            'isbn': 'ISBN',
            'pdf': 'Upload PDF',
            'purchase_link': 'Purchase Link',
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.Select(choices=[(i, f"{i} Stars") for i in range(1, 6)], attrs={
                'class': 'form-select',
                'style': 'border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'
            }),
            'review': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your review',
                'style': 'border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'
            }),
        }
        labels = {
            'rating': 'Rating (Out of 5)',
            'review': 'Review',
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating not in range(1, 6):
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating