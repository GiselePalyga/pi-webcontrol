from django.contrib import admin
from .models import Pagamento

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ["nota_fiscal", "data_pagamento", "valor_pago", "forma_pagamento"]
    list_filter = ["forma_pagamento"]
