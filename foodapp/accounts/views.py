from django.contrib.auth import login, logout
from django.views.generic import TemplateView
from rest_framework import generics, status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import (
    CustomerRegisterSerializer, ClientRegisterSerializer, DeliveryRegisterSerializer,
    LoginSerializer, UserSerializer,
)

# ---------------------------------------------------------------------------
# HTML page views (three separate register/login pages, one per app "side")
# The pages themselves POST to the API views below via fetch()/async-await.
# ---------------------------------------------------------------------------
class CustomerRegisterPage(TemplateView):
    template_name = 'accounts/customer_register.html'


class CustomerLoginPage(TemplateView):
    template_name = 'accounts/customer_login.html'


class ClientRegisterPage(TemplateView):
    template_name = 'accounts/client_register.html'


class ClientLoginPage(TemplateView):
    template_name = 'accounts/client_login.html'


class DeliveryRegisterPage(TemplateView):
    template_name = 'accounts/delivery_register.html'


class DeliveryLoginPage(TemplateView):
    template_name = 'accounts/delivery_login.html'


# ---------------------------------------------------------------------------
# REST API (POST) — register / login / logout, one triplet per user type
# ---------------------------------------------------------------------------
def _issue_session_and_token(request, user):
    login(request, user)  # session auth, so normal Django/admin pages also work
    token, _ = Token.objects.get_or_create(user=user)
    return token


class BaseRegisterAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = _issue_session_and_token(request, user)
        return Response({
            'message': 'Registration successful.',
            'token': token.key,
            'user': UserSerializer(user).data,
            'redirect_url': _redirect_for(user),
        }, status=status.HTTP_201_CREATED)


class CustomerRegisterAPIView(BaseRegisterAPIView):
    serializer_class = CustomerRegisterSerializer


class ClientRegisterAPIView(BaseRegisterAPIView):
    serializer_class = ClientRegisterSerializer


class DeliveryRegisterAPIView(BaseRegisterAPIView):
    serializer_class = DeliveryRegisterSerializer


def _redirect_for(user):
    return {
        User.CUSTOMER: '/',
        User.CLIENT: '/client/dashboard/',
        User.DELIVERY: '/delivery/dashboard/',
        User.ADMIN: '/admin/',
    }.get(user.user_type, '/')


class LoginAPIView(APIView):
    """
    Shared login endpoint used by all three login pages. Each page only
    lets its own user_type in, so a delivery boy can't log in from the
    customer page even with correct credentials.
    """
    permission_classes = [permissions.AllowAny]
    allowed_user_type = None  # overridden per subclass

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if self.allowed_user_type and user.user_type != self.allowed_user_type:
            return Response(
                {'message': f"This account isn't registered as a {self.allowed_user_type}."},
                status=status.HTTP_403_FORBIDDEN,
            )

        token = _issue_session_and_token(request, user)
        return Response({
            'message': f'Welcome back, {user.username}!',
            'token': token.key,
            'user': UserSerializer(user).data,
            'redirect_url': _redirect_for(user),
        })


class CustomerLoginAPIView(LoginAPIView):
    allowed_user_type = User.CUSTOMER


class ClientLoginAPIView(LoginAPIView):
    allowed_user_type = User.CLIENT


class DeliveryLoginAPIView(LoginAPIView):
    allowed_user_type = User.DELIVERY


class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        logout(request)
        return Response({'message': 'Logged out successfully.', 'redirect_url': '/'})


class CurrentUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
