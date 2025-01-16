from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'books'  # Use app namespace to avoid conflicts in larger projects

urlpatterns = [
    # Home page, redirects to book list
    path('', views.home, name='home'),
    
    # Book detail view
    path('books/<int:pk>/', login_required(views.book_detail), name='book_detail'),

    # Book upload
    path('books/upload/', login_required(views.upload_book), name='upload_book'),

    # Book list view
    path('books/', views.book_list, name='book_list'),

    # User login/logout views
    path('login/', views.custom_login, name='custom_login'),
    path('logout/', views.custom_logout, name='custom_logout'),

    # User registration
    path('register/', views.register, name='register'),

    # Book trends
    path('trends/', views.book_trends, name='book_trends'),

    # Search functionality
    path('search/', views.search_books, name='search_books'),

    # Advanced filtering
    path('books/filter/<str:category>/', views.filter_books_by_category, name='filter_books_by_category'),

    # API endpoints (if applicable, for future scalability)
    path('api/books/', views.api_book_list, name='api_book_list'),
    path('api/books/<int:pk>/', views.api_book_detail, name='api_book_detail'),

    path('search/', views.search_books, name='search_books'),
    path('recommendations/', views.get_recommendations, name='get_recommendations'),
]