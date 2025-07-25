from django.db import models

class IndicadorINE(models.Model):
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=255)
    año = models.IntegerField()
    mes = models.IntegerField()
    valor = models.FloatField()

    class Meta:
        unique_together = ('codigo', 'año', 'mes')

    def __str__(self):
        return f"{self.nombre} - {self.mes}/{self.año}"
