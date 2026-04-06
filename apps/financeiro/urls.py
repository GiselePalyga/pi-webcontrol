from django.urls import path
from . import views

app_name = "financeiro"

urlpatterns = [
    path("pagamento/nota/<int:nota_pk>/", views.registrar_pagamento, name="registrar"),
    path("pagamento/<int:pk>/excluir/", views.excluir_pagamento, name="excluir"),
]
