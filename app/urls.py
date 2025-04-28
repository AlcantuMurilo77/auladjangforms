from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
]