from django.core.management.base import BaseCommand

from cristobalcolon.models import Usuario, Mision, Exoplaneta


class Command(BaseCommand):
    help = 'Comprueba que los datos de prueba cumplen las reglas del proyecto'

    def handle(self, *args, **options):
        errores = 0

        # 1. Cada mision tiene la nave llena y los capitanes que le tocan
        self.stdout.write('--- Misiones ---')
        for mision in Mision.objects.all():
            nave = mision.nave
            participantes = mision.participantes.count()
            capitanes = mision.participantes.filter(capitan=True).count()

            self.stdout.write(
                mision.estado + ' | ' + nave.tamanio
                + ' | capacidad: ' + str(nave.capacidad)
                + ' | participantes: ' + str(participantes)
                + ' | capitanes: ' + str(capitanes)
                + ' | exoplanetas: ' + str(mision.exoplanetas.count())
            )

            if not nave.capacidad_valida():
                self.stdout.write('  ERROR: la capacidad no corresponde al tamanio')
                errores += 1
            if participantes != nave.capacidad:
                self.stdout.write('  ERROR: la nave no va llena')
                errores += 1
            if capitanes != nave.capitanes_requeridos():
                self.stdout.write('  ERROR: numero de capitanes incorrecto')
                errores += 1

        # 2. Ningun usuario esta en dos misiones en curso a la vez
        self.stdout.write('--- Usuarios ---')
        repetidos = 0
        for usuario in Usuario.objects.all():
            if usuario.misiones.filter(estado='En curso').count() > 1:
                self.stdout.write('  ERROR: ' + usuario.apodo + ' esta en varias misiones en curso')
                repetidos += 1
        self.stdout.write('Usuarios en mas de una mision en curso: ' + str(repetidos))
        errores += repetidos

        # 3. Solo las misiones con exito tienen exoplanetas
        self.stdout.write('--- Exoplanetas ---')
        mal = Exoplaneta.objects.exclude(mision__estado='Exitosa').count()
        self.stdout.write('Exoplanetas en misiones sin exito: ' + str(mal))
        errores += mal

        if errores == 0:
            self.stdout.write('TODO CORRECTO')
        else:
            self.stdout.write('Hay ' + str(errores) + ' errores')