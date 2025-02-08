from rest_framework import permissions
from .serializers import RoleSerializer,UserSerializer
from.models import Role, User
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password,make_password
class RoleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '').strip().lower()  # Normalize username
        password = request.data.get('password', '')

        if not username or not password:
            return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        print(f"Attempting login: username={username}")

        # Try authenticating the user
        user = authenticate(request, username=username, password=password)

        # If authentication fails, check manually (useful for debugging)
        if user is None:
            try:
                user = User.objects.get(username=username)
                if not check_password(password, user.password):  # Verify password manually
                    raise AuthenticationFailed("Invalid credentials.")
            except User.DoesNotExist:
                raise AuthenticationFailed("Invalid credentials.")

        # Ensure the user is allowed to log in
        if not user.can_login:
            raise AuthenticationFailed("Your account is disabled from logging in.")

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Serialize user data
        serialized_user = UserSerializer(user).data

        return Response({
            "user": serialized_user,
            "access": access_token,
            "refresh": str(refresh),
        }, status=status.HTTP_200_OK)