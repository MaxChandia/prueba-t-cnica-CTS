from django.urls import path
from .views import RegisterAPIView, EmailVerificationAPIView, UserListAPIView, WinnerManagementAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Ruta para el registro de nuevos usuarios
    
    path('registro/', RegisterAPIView.as_view(), name='api-registro'),
    
    # Rutas para la autenticación JWT
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Ruta para la verificación de email y creación de contraseña
    
    path('verificar-email/', EmailVerificationAPIView.as_view(), name='api-verificar-email'),
    
    # Ruta para que el admin liste a todos los usuarios
    
    path('usuarios/', UserListAPIView.as_view(), name='api-usuarios'),
    
    # Ruta para que el admin gestione a los ganadores
    
    path('ganadores/', WinnerManagementAPIView.as_view(), name='api-ganadores'),
]