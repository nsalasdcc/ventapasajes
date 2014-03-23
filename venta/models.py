from django.db import models


class Ciudad(models.Model):
    nombre = models.CharField(max_length=100, primary_key=True)


class Conductor(models.Model):
    rut = models.CharField(max_length=12, primary_key=True)
    nombre = models.CharField(max_length=100)


class Bus(models.Model):
    patente = models.CharField(max_length=10, primary_key=True)
    capacidad = models.IntegerField()
    rut_conductor = models.ForeignKey(Conductor)


class Recorrido(models.Model):
    id_recorrido = models.AutoField(primary_key=True)
    origen = models.ForeignKey(Ciudad, related_name='ciudad_origen')
    destino = models.ForeignKey(Ciudad, related_name='ciudad_destino')
    hora_inicio = models.DateTimeField()
    hora_llegada = models.DateTimeField()
    bus_asignado = models.ForeignKey(Bus)
