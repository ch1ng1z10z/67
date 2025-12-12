from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from .models import CustomUser

# ---------------- Register ----------------
class RegisterView(APIView):
    def post(self, request):
        data = request.data

        email = data.get("email")
        password = data.get("password")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        birthdate = data.get("birthdate")  # формат YYYY-MM-DD

        if not email or not password:
            return Response({"error": "Email и пароль обязательны"},
                            status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "Пользователь с таким email уже существует"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            birthdate=birthdate,
            password=make_password(password),
            is_active=True
        )

        return Response({
            "message": "Пользователь зарегистрирован",
            "email": user.email
        }, status=status.HTTP_201_CREATED)


# ---------------- Login ----------------
class LoginView(APIView):
    def post(self, request):
        data = request.data

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return Response({"error": "Email и пароль обязательны"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        if not user:
            return Response({"error": "Неверные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)

        return Response({
            "message": "Вход выполнен",
            "email": user.email
        })
