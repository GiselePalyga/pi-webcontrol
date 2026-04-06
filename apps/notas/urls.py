from django.urls import path
from . import views

app_name = "notas"

urlpatterns = [
    path("", views.lista, name="lista"),
    path("nova/", views.novo, name="novo"),
    path("<int:pk>/", views.detalhe, name="detalhe"),
    path("<int:pk>/editar/", views.editar, name="editar"),
]
