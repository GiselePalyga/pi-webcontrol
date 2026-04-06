from django import forms
from .models import Pagamento


class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ["data_pagamento", "valor_pago", "forma_pagamento", "observacoes"]
        widgets = {
            "data_pagamento": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "valor_pago": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.01"}),
            "forma_pagamento": forms.Select(attrs={"class": "form-select"}),
            "observacoes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
