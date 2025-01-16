from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from .models import Book, Rating
from django.db.models import Avg
from django.shortcuts import redirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookForm, RatingForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from datetime import datetime
from django.http import Http404
from .recommendations import recommend_books_hybrid
from .models import SearchHistory


# Book list view with search and filtering
def book_list(request):
    query = request.GET.get('q', '').strip()  # Search query
    category = request.GET.get('category', '').strip()  # Category filter
    author = request.GET.get('author', '').strip()  # Author filter

    # Retrieve all books
    books = Book.objects.all()

    # Apply filters based on query parameters
    if query:
        books = books.filter(
            Q(book_name__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query) |
            Q(title__icontains=query)
        )
    if category:
        books = books.filter(category__icontains=category)
    if author:
        books = books.filter(author__icontains=author)

    return render(request, 'books/book_list.html', {
        'books': books,
        'query': query,
        'category': category,
        'author': author,
    })


# Book detail view with rating and review functionality
@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if hasattr(book, 'image') and not book.image:
        book.image = "books/images/default.jpg"

    # Handle form submission for ratings and reviews
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.book = book
            rating.user = request.user
            rating.save()
            return redirect('books:book_detail', pk=book.pk)
    else:
        form = RatingForm()

    # Calculate the book's average rating and total reviews
    average_rating = book.ratings.aggregate(avg=Avg('rating'))['avg']
    total_reviews = book.ratings.count()

    return render(request, 'books/book_detail.html', {
        'book': book,
        'form': form,
        'average_rating': average_rating,
        'total_reviews': total_reviews,
    })


# Home view redirects to the book list
def home(request):
    return redirect('books:book_list')


# Book upload view
@login_required
def upload_book(request):
    if not request.user.is_superuser:
        return redirect('books:book_list')

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('books:book_list')
    else:
        form = BookForm()

    return render(request, 'books/upload_book.html', {'form': form})


# Custom login view
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'})
    return render(request, 'books/login.html')


# Registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books:custom_login')
    else:
        form = UserCreationForm()
    return render(request, 'books/register.html', {'form': form})


# Book trends view to show top-rated books
def book_trends(request):
    # Annotate books with average ratings
    top_books = Book.objects.annotate(
        avg_rating=Avg('ratings__rating')
    ).order_by('-avg_rating')[:10]
    return render(request, 'books/trends.html', {'top_books': top_books})


# Custom logout view
@login_required
def custom_logout(request):
    logout(request)
    return redirect('books:custom_login')

@login_required
def get_recommendations(request):
    recommendations = recommend_books_hybrid(request.user)
    return render(request, 'books/recommendations.html', {'recommendations': recommendations})


# Book search view
def search_books(request):
    query = request.GET.get('q', '').strip()  # Get the search query and strip whitespace
    user = request.user if request.user.is_authenticated else None

    # Save search query to history
    if user and query:
        print(f"Saving search query: {query} for user: {user}")
        SearchHistory.objects.create(user=user, query=query)
    books = Book.objects.filter(
            Q(book_name_icontains=query) | Q(author_icontains=query) | Q(title__icontains=query) | Q(category__icontains=query)
        ) if query else []
    
    return render(request, 'books/search_results.html', {  # Ensure template path matches your structure
        'books': books,
        'query': query,
        'current_year': datetime.now().year,
    })

def filter_books_by_category(request):
    category = request.GET.get('category', '')  # Get the category from the request
    books = Book.objects.filter(category__icontains=category) if category else []
    return render(request, 'books/filter_results.html', {
        'category': category,
        'books': books,
        'current_year': datetime.now().year,
    })

def api_book_list(request):
    books = Book.objects.all().values('id', 'book_name', 'author', 'category', 'publication_year')
    return JsonResponse(list(books), safe=False)

def api_book_detail(request, book_id):
    try:
        # Retrieve the book with the given ID
        book = Book.objects.values('id', 'book_name', 'author', 'category', 'publication_year').get(id=book_id)
        return JsonResponse(book, safe=False)
    except Book.DoesNotExist:
        # Return a 404 error if the book is not found
        raise Http404("Book not found")


# Error handling views
def error_404_view(request, exception):
    return render(request, '404.html', status=404)


def error_500_view(request):
    return render(request, '500.html', status=500)
# Test 500 Error View
def test_error(request):
    raise Exception("Test 500 error")

