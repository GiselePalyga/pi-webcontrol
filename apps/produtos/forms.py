from django import forms
from .models import Produto

_fc = "form-control"
_fs = "form-select"
_num = {"class": _fc, "step": "0.01", "min": "0"}
_pct = {"class": _fc, "step": "0.01", "min": "0", "max": "100"}


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            "nome", "unidade_medida", "preco_custo", "preco_venda",
            "estoque_atual", "estoque_minimo",
            "ncm", "cest", "origem",
            "aliquota_icms", "aliquota_ipi", "aliquota_pis", "aliquota_cofins",
            "ativo",
        ]
        widgets = {
            "nome":           forms.TextInput(attrs={"class": _fc, "placeholder": "Nome do produto"}),
            "unidade_medida": forms.Select(attrs={"class": _fs}),
            "preco_custo":    forms.NumberInput(attrs=_num),
            "preco_venda":    forms.NumberInput(attrs=_num),
            "estoque_atual":  forms.NumberInput(attrs={"class": _fc, "step": "0.001", "min": "0"}),
            "estoque_minimo": forms.NumberInput(attrs={"class": _fc, "step": "0.001", "min": "0"}),
            "ncm":            forms.TextInput(attrs={"class": _fc, "placeholder": "0000.00.00", "data-mask": "ncm", "maxlength": "10"}),
            "cest":           forms.TextInput(attrs={"class": _fc, "placeholder": "00.000.00", "data-mask": "cest", "maxlength": "9"}),
            "origem":         forms.Select(attrs={"class": _fs}),
            "aliquota_icms":  forms.NumberInput(attrs=_pct),
            "aliquota_ipi":   forms.NumberInput(attrs=_pct),
            "aliquota_pis":   forms.NumberInput(attrs=_pct),
            "aliquota_cofins":forms.NumberInput(attrs=_pct),
            "ativo":          forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
