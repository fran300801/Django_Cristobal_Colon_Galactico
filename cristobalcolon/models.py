from django.db import models
from django.core.exceptions import ValidationError

class Exoplaneta(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    mision = models.ForeignKey(
        'Mision',
        on_delete=models.CASCADE,
        related_name='exoplanetas'
    )
    fecha_descubrimiento = models.DateField(auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True)

    def validar_mision_exitosa(self):
        if self.mision and not self.mision.exitosa:
            raise ValidationError(
                "No se puede registrar un exoplaneta para una misión que no ha tenido éxito."
            )

    def clean(self):
        self.validar_mision_exitosa()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Caracteristica(models.Model):
    OPCIONES_CARACTERISTICA = [
        ('Misiones largas', 'Misiones largas'),
        ('Explorador de cortas distancias', 'Explorador de cortas distancias'),
        ('Conflictivo', 'Conflictivo'),
        ('Cocinero', 'Cocinero'),
        ('Mantenimiento', 'Mantenimiento'),
    ]

    nombre = models.CharField(
            max_length=50,
        choices=OPCIONES_CARACTERISTICA,
        unique=True
    )
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre