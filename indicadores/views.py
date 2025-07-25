from django.shortcuts import render

def dashboard(request):
    fechas = ["01/2023", "02/2023", "03/2023", "04/2023", "05/2023"]
    valores = [60.5, 62.3, 64.1, 63.8, 65.2]
    # ATENCIÓN: aquí solo dashboard.html, sin prefijo de app/indicadores
    return render(request, "dashboard.html", {
        "fechas": fechas,
        "valores": valores,
    })
