# indicadores/management/commands/import_ine.py

import requests
import datetime

from django.core.management.base import BaseCommand, CommandError
from indicadores.models import IndicadorINE

class Command(BaseCommand):
    help = 'Importa datos de una serie del INE a la tabla IndicadorINE'

    def add_arguments(self, parser):
        parser.add_argument(
            'codigo_serie',
            type=str,
            help='Código de la serie INE (p.ej. CP335)'
        )

    def handle(self, *args, **options):
        codigo = options['codigo_serie']
        self.stdout.write(self.style.SUCCESS(f'Importando datos para la serie: {codigo}'))

        # 1) Construir la URL y llamar a la API
        url = f'https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/{codigo}?nult=999'
        response = requests.get(url)
        if response.status_code != 200:
            raise CommandError(f'Error al llamar a la API (status {response.status_code})')

        # 2) Parsear JSON
        datos = response.json()
        nombre_serie = datos.get('Nombre', 'SIN NOMBRE')
        registros = datos.get('Data', [])
        self.stdout.write(self.style.SUCCESS(
            f'  → Serie "{nombre_serie}" con {len(registros)} datos'
        ))

        # 3) Guardar cada registro en la BD
        for item in registros:
            # Fecha viene en milisegundos desde Epoch
            ts = item.get('Fecha', 0)
            fecha = datetime.date.fromtimestamp(ts // 1000)
            año = fecha.year
            mes = fecha.month
            valor = item.get('Valor', None)

            # update_or_create evita duplicados según la clave única
            obj, created = IndicadorINE.objects.update_or_create(
                codigo=codigo,
                año=año,
                mes=mes,
                defaults={
                    'nombre': nombre_serie,
                    'valor': valor,
                }
            )

            # Mensaje por cada inserción/actualización (opcional)
            action = 'Creado' if created else 'Actualizado'
            self.stdout.write(f'    - {action}: {codigo} {mes}/{año} = {valor}')

        self.stdout.write(self.style.SUCCESS('¡Importación completada!'))
