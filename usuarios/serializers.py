from rest_framework import serializers
from .models import User
from django.core.signing import Signer

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=None,
            **validated_data
        )

        signer = Signer()
        token = signer.sign(user.email)
        print(f"\nPor favor, verifica tu email con este token: {token}\n")

        return user

class PasswordCreationSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)

# Creamos los validadores para el registro de usuarios y generamos el token de verificación para el email.
# También creamos el serializador para la creación de la contraseña a partir del token enviado al email.