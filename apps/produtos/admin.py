from django.contrib import admin
from .models import Produto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ["nome", "unidade_medida", "preco_custo", "preco_venda", "estoque_atual", "ativo"]
    list_filter = ["ativo", "unidade_medida"]
    search_fields = ["nome"]
