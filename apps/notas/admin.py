from django.contrib import admin
from .models import NotaFiscal, ItemNotaFiscal

class ItemInline(admin.TabularInline):
    model = ItemNotaFiscal
    extra = 0

@admin.register(NotaFiscal)
class NotaFiscalAdmin(admin.ModelAdmin):
    list_display = ["numero", "serie", "fornecedor", "data_emissao", "data_vencimento", "valor_total", "status"]
    list_filter = ["status"]
    search_fields = ["numero", "fornecedor__nome_fantasia"]
    inlines = [ItemInline]
