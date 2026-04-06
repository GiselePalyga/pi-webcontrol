from django.contrib import admin
from .models import Fornecedor

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ["nome_fantasia", "cnpj", "cidade", "uf", "ativo"]
    list_filter = ["ativo", "uf"]
    search_fields = ["nome_fantasia", "razao_social", "cnpj"]
