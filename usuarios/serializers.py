from rest_framework import serializers
from .models import User
from django.core.signing import Signer


class UserRegistrationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=True) 

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number']

    def validate_phone_number(self, value):
        if len(value) != 12:
            raise serializers.ValidationError("El número de teléfono debe tener 12 caracteres (+569 y 8 dígitos).")
        if not value.startswith('+569'):
            raise serializers.ValidationError("El número de teléfono debe empezar con +569.")
        if not value[4:].isdigit():
            raise serializers.ValidationError("El número de teléfono solo puede contener dígitos después del prefijo.")

        return value

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number']

    def create(self, validated_data):
        email = validated_data.pop('email')
        user = User.objects.create_user(
            email=email,
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
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'phone_number', 'is_verified', 'is_winner']

# Creamos los validadores para el registro de usuarios y generamos el token de verificación para el email, además el serializador para el listado de usuarios.
# También creamos el serializador para la creación de la contraseña a partir del token enviado al email.