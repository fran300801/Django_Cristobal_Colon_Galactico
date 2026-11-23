import random

from django.db import models
from faker import Faker

fake = Faker('es_ES')

# Create your models here.

class Usuario(models.Model):
    apodo = models.CharField(max_length=100)
    habilidad_arma = models.IntegerField(default=0)
    habilidad_conduccion = models.IntegerField(default=0)
    capitan = models.BooleanField(default=False)
    caracteristicas = models.ManyToManyField(Caracteristica, blank=True)

    def __str__(self):
        return self.apodo


class Nave(models.Model):
    nombre = models.CharField(max_length=100)
    tamanio = models.CharField(max_length=50)
    capacidad = models.IntegerField()

    def capitanes_requeridos(self):
        if self.tamanio == 'Grande':
            return 2
        return 1

    def capacidad_valida(self):
        if self.tamanio == 'Pequeña':
            return self.capacidad == 4
        if self.tamanio == 'Mediana':
            return 8 <= self.capacidad <= 10
        if self.tamanio == 'Grande':
            return 11 <= self.capacidad <= 30
        return False

    def __str__(self):
        return self.nombre

class Mision(models.Model):
    nombre = models.CharField(max_length=100)
    nave = models.ForeignKey(Nave, on_delete=models.PROTECT)
    participantes = models.ManyToManyField(Usuario, related_name='misiones')
    estado = models.CharField(max_length=50, default='En curso')
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Mision"
        verbose_name_plural = "Misiones"