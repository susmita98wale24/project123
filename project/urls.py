"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('books/', login_required(views.book_list), name='book_list'),
    path('books/<int:pk>/', login_required(views.book_detail), name='book_detail'),
    path('books/upload/', views.upload_book, name='upload_book'),
    path('custom-login/', views.custom_login, name='custom_login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('register/', views.register, name='register'),
    path('books/',include('app.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('trends/', views.book_trends, name='book_trends'),
    path('search/', views.search_books, name='search_books'),
] 

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom Error Handlers
handler404 = 'app.views.error_404_view'
handler500 = 'app.views.error_500_view'
