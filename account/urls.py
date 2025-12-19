from django.urls import path
from .views import RegisterView, JWTLoginView, GoogleLoginView, GoogleCallbackView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', JWTLoginView.as_view(), name='jwt_login'),
    path('oauth/google/login/', GoogleLoginView.as_view(), name='google_login'),
    path('oauth/google/callback/', GoogleCallbackView.as_view(), name='google_callback'),
]
