from django import forms
from .models import Produto

_fc  = "form-control"
_fs  = "form-select"
_dec = {"class": _fc, "data-mask": "decimal",    "placeholder": "0,00"}
_pct = {"class": _fc, "data-mask": "decimal",    "placeholder": "0,00"}
_qty = {"class": _fc, "data-mask": "quantidade", "placeholder": "0,000"}


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
            "nome":            forms.TextInput(attrs={"class": _fc, "placeholder": "Nome do produto"}),
            "unidade_medida":  forms.Select(attrs={"class": _fs}),
            "preco_custo":     forms.TextInput(attrs=_dec),
            "preco_venda":     forms.TextInput(attrs=_dec),
            "estoque_atual":   forms.TextInput(attrs=_qty),
            "estoque_minimo":  forms.TextInput(attrs=_qty),
            "ncm":             forms.TextInput(attrs={"class": _fc, "placeholder": "0000.00.00", "data-mask": "ncm", "maxlength": "10"}),
            "cest":            forms.TextInput(attrs={"class": _fc, "placeholder": "00.000.00", "data-mask": "cest", "maxlength": "9"}),
            "origem":          forms.Select(attrs={"class": _fs}),
            "aliquota_icms":   forms.TextInput(attrs=_pct),
            "aliquota_ipi":    forms.TextInput(attrs=_pct),
            "aliquota_pis":    forms.TextInput(attrs=_pct),
            "aliquota_cofins": forms.TextInput(attrs=_pct),
            "ativo":           forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
