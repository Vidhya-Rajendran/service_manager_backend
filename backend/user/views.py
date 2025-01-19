from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.contrib.auth.models import User


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if username == settings.HARDCODED_USERNAME and password == settings.HARDCODED_PASSWORD:
            user, _ = User.objects.get_or_create(username=username, defaults={"is_staff": True, "is_superuser": True})
            
            refresh = RefreshToken.for_user(user)
            refresh["role"] = "admin"  
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
