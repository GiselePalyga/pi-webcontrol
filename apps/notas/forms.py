from django import forms
from django.forms import inlineformset_factory
from .models import NotaFiscal, ItemNotaFiscal
from apps.fornecedores.models import Fornecedor


class NotaFiscalForm(forms.ModelForm):
    class Meta:
        model = NotaFiscal
        fields = [
            "numero", "serie", "fornecedor",
            "data_emissao", "data_vencimento",
            "valor_total", "status", "observacoes",
        ]
        widgets = {
            "numero": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex: 001234"}),
            "serie": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex: 1"}),
            "fornecedor": forms.Select(attrs={"class": "form-select"}),
            "data_emissao": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "data_vencimento": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "valor_total": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.01"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "observacoes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fornecedor"].queryset = Fornecedor.objects.filter(ativo=True)

    def clean(self):
        cleaned_data = super().clean()
        emissao = cleaned_data.get("data_emissao")
        vencimento = cleaned_data.get("data_vencimento")
        if emissao and vencimento and vencimento < emissao:
            self.add_error("data_vencimento", "A data de vencimento não pode ser anterior à data de emissão.")
        return cleaned_data


class ItemNotaFiscalForm(forms.ModelForm):
    class Meta:
        model = ItemNotaFiscal
        fields = ["produto", "descricao", "quantidade", "valor_unitario"]
        widgets = {
            "produto": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "descricao": forms.TextInput(attrs={"class": "form-control form-control-sm", "placeholder": "Descrição do item"}),
            "quantidade": forms.NumberInput(attrs={"class": "form-control form-control-sm", "step": "0.001", "min": "0.001"}),
            "valor_unitario": forms.NumberInput(attrs={"class": "form-control form-control-sm", "step": "0.01", "min": "0.01"}),
        }


ItemFormSet = inlineformset_factory(
    NotaFiscal,
    ItemNotaFiscal,
    form=ItemNotaFiscalForm,
    extra=1,
    can_delete=True,
    min_num=0,
)


class NotaFiscalFiltroForm(forms.Form):
    busca = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Número, fornecedor..."}),
    )
    status = forms.ChoiceField(
        required=False,
        choices=[("", "Todos os status")] + NotaFiscal.STATUS_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    data_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    data_fim = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
