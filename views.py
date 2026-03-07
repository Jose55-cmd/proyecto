from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Polizas, Clientes, Siniestros # pyright: ignore[reportUnknownVariableType, reportMissingImports]

@login_required  # Esto obliga a que el usuario deba estar logueado
def dashboard_view(request): # type: ignore
    # Lógica: Vamos a contar datos para mostrarlos en el Dashboard
    total_polizas = Polizas.objects.filter(activo=True).count() # type: ignore
    total_clientes = Clientes.objects.count() # type: ignore
    siniestros_pendientes = Siniestros.objects.filter(id_estatus__nombre='Pendiente').count() # type: ignore
    
    context = { # type: ignore
        'total_polizas': total_polizas,
        'total_clientes': total_clientes,
        'siniestros_pendientes': siniestros_pendientes,
    }
    
    return render(request, 'dashboard.html', context) # type: ignore
