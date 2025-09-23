from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    full_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_winner = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

# Creamos el modelo User para los usuarios (Concursantes y Administradores) extendiendo AbstractUser para aprovechar las funcionalidades de autenticación de Django. 
# Añadimos los campos adicionales solicitados y configuramos el campo email como el identificador único para el inicio de sesión.
# full_name y phone_number son opcionales, ya que solo los concursantes los necesitan.