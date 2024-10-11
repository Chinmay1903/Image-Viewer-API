from django.urls import path
from .views import RegisterView, LoginView, TokenVerify

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-token/', TokenVerify.as_view(), name='verify-token'),
]