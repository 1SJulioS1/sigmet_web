from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, empresa, rol, fecha_licencia, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not empresa:
            raise ValueError('Users must have an empresa')
        if not rol:
            raise ValueError('Users must have an rol')
        user = self.model(
            email=self.normalize_email(email),
            empresa=EmpresaId.objects.get(id=empresa),
            rol=rol,
            fecha_licencia=fecha_licencia
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, empresa, rol, password=None):
        user = self.create_user(
            email=email,
            empresa=empresa,
            rol=rol,
            fecha_licencia=None,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    ROL = [
        ('Administrador', 'Administrador'),
        ('Ejecutivo', 'Ejecutivo'),
        ('Operador', 'Operador'),
    ]
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    empresa = models.ForeignKey('EmpresaId', on_delete=models.CASCADE)
    fecha_licencia = models.DateField(blank=True, null=True)
    rol = models.CharField(choices=ROL, max_length=255)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['empresa', 'rol']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class EmpresaId(models.Model):
    nombre = models.TextField()
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresa"

    def __str__(self):
        return self.nombre

    def get_nombre(self):
        return self.nombre

    def get_id(self):
        return self.id
