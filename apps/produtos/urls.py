from django.urls import path
from . import views

app_name = "produtos"

urlpatterns = [
    path("", views.lista, name="lista"),
    path("novo/", views.novo, name="novo"),
    path("<int:pk>/editar/", views.editar, name="editar"),
    path("<int:pk>/toggle/", views.toggle_ativo, name="toggle"),
]
