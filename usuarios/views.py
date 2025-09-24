from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.signing import Signer, BadSignature
from django.core.mail import send_mail
from .models import User
from .serializers import UserRegistrationSerializer, PasswordCreationSerializer, UserSerializer

# Vista para el registro de nuevos concursantes

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Usuario registrado exitosamente. Por favor, verifica tu email para crear una contraseña."}, status=status.HTTP_201_CREATED)

# Vista para validar el email y crear la contraseña

class EmailVerificationAPIView(APIView):
    def get(self, request, *args, **kwargs):
        token = request.query_params.get('token', '')
        signer = Signer()
        try:
            email = signer.unsign(token)
            return Response({"message": "Token válido. Por favor, ingresa tu contraseña."}, status=status.HTTP_200_OK)
        except BadSignature:
            return Response({"error": "Token de verificación inválido."}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request, *args, **kwargs):
        serializer = PasswordCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        password = serializer.validated_data['password']

        signer = Signer()
        try:
            email = signer.unsign(token)
            user = User.objects.get(email=email)

            if user.is_verified:
                return Response({"message": "Este email ya ha sido verificado."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(password)
            user.is_verified = True
            user.save()

            return Response({"message": "Email verificado y contraseña establecida correctamente."}, status=status.HTTP_200_OK)

        except BadSignature:
            return Response({"error": "Token de verificación inválido."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)


# Vista para que el admin liste a todos los usuarios

class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


# Vista para que el admin administre a los ganadores

class WinnerManagementAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            user.is_winner = True
            user.save()

            # Lógica para enviar el correo electrónico al ganador
            send_mail(
                '¡Felicidades, eres un ganador!',
                '¡Hola! Nos complace informarte que has sido seleccionado como ganador en nuestro concurso. ¡Felicidades!',
                'tu_correo@ejemplo.com',
                [user.email],
                fail_silently=False,
            )

            return Response({"message": f"El usuario {email} ha sido marcado como ganador y notificado por correo."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)