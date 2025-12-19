from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth import login

from rest_framework_simplejwt.views import TokenObtainPairView
from .jwt import CustomTokenSerializer
from .models import CustomUser

import requests



class JWTLoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer


class RegisterView(APIView):
    def post(self, request):
        data = request.data

        user = CustomUser.objects.create_user(
            email=data["email"],
            password=data["password"],
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            birthdate=data.get("birthdate"),
            is_active=True
        )

        return Response({"message": "registered"})


class GoogleLoginView(APIView):
    def get(self, request):
        url = (
            "https://accounts.google.com/o/oauth2/v2/auth"
            f"?client_id={settings.GOOGLE_CLIENT_ID}"
            f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
            "&response_type=code"
            "&scope=openid email profile"
        )
        return redirect(url)


class GoogleCallbackView(APIView):
    def get(self, request):
        code = request.GET.get("code")

        token_resp = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            }
        ).json()

        access_token = token_resp.get("access_token")

        userinfo = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        ).json()

        user, _ = CustomUser.objects.get_or_create(email=userinfo["email"])

        user.first_name = userinfo.get("given_name")
        user.last_name = userinfo.get("family_name")
        user.google_id = userinfo["sub"]
        user.is_active = True
        user.last_login = timezone.now()
        user.save()

        login(request, user)
        return Response({"message": "google login success"})
