import random

from django.db import models
from faker import Faker

fake = Faker('es_ES')

CARACTERISTICAS = [
    'Misiones largas',
    'Explorador de cortas distancias',
    'Conflictivo',
    'Cocinero',
    'Mantenimiento',
]

TAMANIOS = [
    'Grande',
    'Mediana',
    'Pequeña'
]

# Create your models here.

def random_habilidad():
    return random.randint(0, 100)

def random_apodo():
    return fake.user_name()

def random_caracteristica_principal():
    return random.choice(CARACTERISTICAS)

def random_capacidad():
    return random.randint(4, 30)

class Usuario(models.Model):
    apodo = models.CharField(default=random_apodo, max_length=100)
    habilidad_arma = models.IntegerField(default=random_habilidad)
    habilidad_conduccion = models.IntegerField(default=random_habilidad)
    caracteristica_principal = models.CharField(default=random_caracteristica_principal, max_length=100)
    capitan = models.BooleanField(default=False)


class Nave(models.Model):
    nombre = models.CharField(max_length=100)
    tamanio = models.CharField(default='Mediana' ,max_length=100)
    capacidad = models.IntegerField(default=random_capacidad)

    def definir_tamanio(self):
        if self.capacidad <= 7:
            return 'Pequeña'
        elif self.capacidad <= 10:
            return 'Mediana'
        elif self.capacidad <= 30:
            return 'Grande'

class Mision(models.Model):
    nombre = models.CharField(max_length=100)
    nave = models.ForeignKey(Nave, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    exito = models.BooleanField(default=False)
    class Meta:
        verbose_name = "Mision"
        verbose_name_plural = "Misiones"