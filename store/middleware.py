
from django.shortcuts import redirect
from django.urls import reverse

class CheckUserLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path != reverse('login') and request.path != reverse('signup') and request.path != reverse('book_list') :
            # Redirect to login page if user is not authenticated
            return redirect('login')
        return self.get_response(request)
