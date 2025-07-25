from django.shortcuts import render
from .models import IndicadorINE
from django.http import JsonResponse

def home(request):
    """
    Vista para la página de inicio.
    """
    # Renderiza templates/home.html
    return render(request, 'home.html')

FILTER_CATEGORIES = {
    'Oferta alojativa': ['EOT55', 'EOT56', 'EOT57', 'EOT58', 'EOT59'],      # hoteles
    'Turismo receptivo': ['EOT17', 'FREG286'],                             # extranjeros y turistas FRONTUR
    'Mercados principales': ['FREG287', 'EOT9'],                           # visitantes totales y nacionales
    'ADR (Tarifa diaria)': ['EOT16414', 'EOT16415'],
    'RevPAR': ['EOT16470', 'EOT16471'],
    'Estancia media': ['EOT2323'],
    'Antelación de reserva': [''],   # aquí puedes añadir el código si lo localizas
    'Países': ['EOT9', 'EOT17'],      # mismo ejemplo: nacionales vs extranjeros
    # ... añade más categorías según necesites
}

def dashboard(request):
    # Lista de (código, nombre) de todas las series en la BD
    all_series = dict(IndicadorINE.objects.values_list('codigo', 'nombre').distinct())
    # Pasamos:
    # - categories: lista de nombres de categoría
    # - series por categoría (diccionario)
    # - all_series: para resolver los nombres al poblar el select
    return render(request, 'dashboard.html', {
        'categories': list(FILTER_CATEGORIES.keys()),
        'series_by_cat': FILTER_CATEGORIES,
        'all_series': all_series,
    })


def datos_indicador(request, codigo):
    """
    Devuelve JSON con listas 'fechas' y 'valores' para el código dado.
    """
    # Recupera registros ordenados
    queryset = IndicadorINE.objects.filter(codigo=codigo).order_by('año', 'mes')
    # Construye las listas
    fechas = [f"{obj.mes}/{obj.año}" for obj in queryset]
    valores = [obj.valor for obj in queryset]
    # Retorna JSON
    return JsonResponse({'fechas': fechas, 'valores': valores})
