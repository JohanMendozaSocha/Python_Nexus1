from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import EmailValidator
from django.db import models



class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        if not username:
            raise ValueError('El usuario debe tener un username')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.AutoField(primary_key=True)

    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)

    email = models.EmailField(unique=True, validators=[EmailValidator()])
    username = models.CharField(max_length=150, unique=True)

    #Elimine en la q se definia la contraseña manualemnte, porq la calse usuario esta heredando de abstractbaseUser,
    #para evitar futuros problemas de q dijango de confunde con cual usar.
    
    # Equivalente a @ManyToOne
    rol = models.ForeignKey(
        'Rol',
        on_delete=models.PROTECT,
        related_name='usuarios',
        null=True, # Lo dejamos temporalmente en True por si creas un superusuario antes de mapear los roles
        blank=True
    )

    estado = models.CharField(max_length=20, default="ACTIVO")
    created_at = models.DateTimeField(auto_now_add=True)

    # Campos obligatorios que Django requiere internamente para el panel de administración
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 

    # Configuración para que Django sepa cómo interactuar con este modelo
    objects = UsuarioManager()

    USERNAME_FIELD = 'username'  # Campo con el que se inicia sesión
    REQUIRED_FIELDS = ['email']  # Campos obligatorios al crear superusuario por consola

    def get_cantidad_eventos(self):
        return self.eventos_creados.count()

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


# Asegúrate de tener tu clase Rol definida abajo para que no te dé error el ForeignKey
class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre