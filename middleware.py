from django.shortcuts import redirect
from django.conf import settings

def admin_only_middleware(get_response):
    """
    Middleware to restrict access to the admin panel for non-superusers.
    """
    def middleware(request):
        if request.path.startswith('/admin/') and not request.user.is_superuser:
            return redirect('/books/')  # Redirect unauthorized users to books page
        return get_response(request)

    return middleware


def theme_selection_middleware(get_response):
    """
    Middleware to dynamically set a theme for the user based on session or cookie data.
    """
    def middleware(request):
        # Check if the user has a preferred theme stored in the session or cookies
        user_theme = request.session.get('theme') or request.COOKIES.get('theme')
        
        # Set a default theme if none is selected
        if not user_theme:
            user_theme = 'modern_theme'
            request.session['theme'] = user_theme

        # Inject the theme into settings for use across the app
        settings.THEME = user_theme

        # Proceed with the response
        response = get_response(request)

        # Optionally set a cookie to persist the theme
        response.set_cookie('theme', user_theme)
        return response

    return middleware


def enforce_https_middleware(get_response):
    """
    Middleware to enforce HTTPS for secure communication.
    """
    def middleware(request):
        if not request.is_secure() and not settings.DEBUG:
            # Redirect to HTTPS version of the requested URL
            secure_url = request.build_absolute_uri().replace('http://', 'https://')
            return redirect(secure_url)
        return get_response(request)

    return middleware