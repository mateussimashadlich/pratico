
from django.shortcuts import redirect


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user or not request.user.is_active:
            if not request.path == '/login' and not request.path == '/usuario/cadastro':
                return redirect('login')
        elif request.user and (request.path == '/login' or request.path == '/usuario/cadastro'):
            return redirect('index')

        response = self.get_response(request)

        return response
