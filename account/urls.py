from django.urls import path
from .views import RegisterView, LoginView, GoogleLoginView, GoogleCallbackView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),

    path('oauth/google/login/', GoogleLoginView.as_view(), name='google_login'),
    path('oauth/google/callback/', GoogleCallbackView.as_view(), name='google_callback'),
]
