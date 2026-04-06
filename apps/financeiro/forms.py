from django import forms
from .models import Pagamento


class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ["data_pagamento", "valor_pago", "forma_pagamento", "observacoes"]
        widgets = {
            "data_pagamento": forms.DateInput(attrs={"class": "form-control", "placeholder": "dd/mm/aaaa", "data-mask": "data"}, format="%d/%m/%Y"),
            "valor_pago": forms.TextInput(attrs={"class": "form-control", "data-mask": "decimal", "placeholder": "0,00"}),
            "forma_pagamento": forms.Select(attrs={"class": "form-select"}),
            "observacoes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
