from django.urls import path
from . import views

urlpatterns = [
    # Cuando el usuario entre a midominio.com/dashboard/
    path('dashboard/', views.dashboard_view, name='dashboard'), # type: ignore
]
