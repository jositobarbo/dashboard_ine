# indicadores/management/commands/import_all_turismo.py

from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Importa en bloque todos los indicadores turísticos nacionales'

    def handle(self, *args, **options):
        # Lista de códigos a importar
        codes = [
            # EOH – ocupación hotelera
            "EOT1","EOT9","EOT17","EOT25","EOT33","EOT41","EOT2323",
            "EOT55","EOT56","EOT57","EOT58","EOT59","EOT60","EOT866","EOT869",
            # IRSH/IIH – rentabilidad hotelera
            "EOT16414","EOT16415","EOT16470","EOT16471","EOT14624","EOT14625","EOT14680","EOT14681",
            # EOAP – apartamentos turísticos
            "EOT1033","EOT1036",
            # EOA – albergues
            "EOT22981","EOT23041",
            # EG – gasto turístico
            "FREG4584439","FREG4584449",
            # FR – fronteras/Visitantes
            "FREG287","FREG286",
        ]

        for code in codes:
            self.stdout.write(self.style.NOTICE(f"\n⟳ Importando serie {code} …"))
            try:
                # Llama al comando import_ine que ya tienes implementado
                call_command('import_ine', code)
            except Exception as e:
                raise CommandError(f"Error al importar {code}: {e}")

        self.stdout.write(self.style.SUCCESS("\n✅ Importación de todos los indicadores completada!"))
