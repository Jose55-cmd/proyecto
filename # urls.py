# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ... tus otras rutas ...
    path('api/crear-perfil/', views.crear_perfil, name='crear_perfil'),
]