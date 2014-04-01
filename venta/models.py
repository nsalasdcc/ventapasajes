from django.db import models


class Ciudad(models.Model):
    nombre = models.CharField(max_length=100, primary_key=True)

    def __unicode__(self):
        return self.nombre


class Conductor(models.Model):
    rut = models.CharField(max_length=12, primary_key=True)
    nombre = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s, rut=%s' % (self.nombre, self.rut)


class Bus(models.Model):
    patente = models.CharField(max_length=10, primary_key=True)
    capacidad = models.IntegerField()
    conductor = models.ForeignKey(Conductor)

    def __unicode__(self):
        return u'patente=%s, capacidad=%s, conducido por %s' % (self.patente, self.capacidad, self.conductor.nombre)


class Recorrido(models.Model):
    id_recorrido = models.AutoField(primary_key=True)
    origen = models.ForeignKey(Ciudad, related_name='ciudad_origen')
    destino = models.ForeignKey(Ciudad, related_name='ciudad_destino')
    hora_inicio = models.DateTimeField()
    hora_llegada = models.DateTimeField()
    bus_asignado = models.ForeignKey(Bus, blank=True, null=True)
    pasajes_vendidos = models.IntegerField()

    def __unicode__(self):
        return u'%s -- %s\t\tsalida=%s' % (self.origen, self.destino, self.hora_inicio)

    def max_capacidad(self):
        return self.bus_asignado.capacidad if self.bus_asignado is not None else 0

    max_capacidad = property(max_capacidad)


class Pasaje(models.Model):
    id_pasaje = models.AutoField(primary_key=True)
    asiento = models.IntegerField(null=True)
    vendido = models.BooleanField(default=False)
    recorrido = models.ForeignKey(Recorrido)