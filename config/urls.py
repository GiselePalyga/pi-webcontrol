from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("dashboard/", include("apps.core.urls")),
    path("fornecedores/", include("apps.fornecedores.urls")),
    path("produtos/", include("apps.produtos.urls")),
    path("notas/", include("apps.notas.urls")),
    path("financeiro/", include("apps.financeiro.urls")),
    path("", RedirectView.as_view(url="/dashboard/", permanent=False)),
]
