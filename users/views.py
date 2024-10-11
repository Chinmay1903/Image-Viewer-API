from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import View
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class RegisterView(View):
    def post(self, request):
        data = json.loads(request.body)

        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': 'Username already exists.'}, status=400)

        # Create a new user
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        return JsonResponse({'message': 'User registered successfully.'}, status=201)

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        username = data.get('username')
        password = data.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Login successful.'
            }, status=200)
        else:
            return JsonResponse({'message': 'Invalid credentials.'}, status=401)

class TokenVerify(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            token = data.get('token')
            UntypedToken(token)  # This will raise an error if the token is invalid
            
            # If token is valid, return a success response
            return JsonResponse({"detail": "Token is valid"}, status=200)
        except (InvalidToken, TokenError):
            return JsonResponse({"detail": "Invalid token"}, status=401)
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=400)
