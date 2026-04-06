import re
from django import forms
from .models import Fornecedor


def validar_cnpj(cnpj):
    cnpj = re.sub(r"\D", "", cnpj)
    if len(cnpj) != 14:
        raise forms.ValidationError("CNPJ deve ter 14 dígitos.")
    if cnpj == cnpj[0] * 14:
        raise forms.ValidationError("CNPJ inválido.")

    def calcular_digito(cnpj, pesos):
        soma = sum(int(c) * p for c, p in zip(cnpj, pesos))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    if calcular_digito(cnpj[:12], pesos1) != int(cnpj[12]):
        raise forms.ValidationError("CNPJ inválido.")
    if calcular_digito(cnpj[:13], pesos2) != int(cnpj[13]):
        raise forms.ValidationError("CNPJ inválido.")
    return cnpj


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = [
            "nome_fantasia", "razao_social", "cnpj", "telefone", "email",
            "cep", "logradouro", "numero", "bairro", "cidade", "uf", "ativo",
        ]
        widgets = {
            "nome_fantasia": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Nome Fantasia",
            }),
            "razao_social": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Razão Social",
            }),
            "cnpj": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "00.000.000/0000-00",
                "data-mask": "cnpj", "maxlength": "18",
            }),
            "telefone": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "(00) 00000-0000",
                "data-mask": "telefone", "maxlength": "15",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control", "placeholder": "email@exemplo.com",
            }),
            "cep": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "00000-000",
                "data-mask": "cep", "maxlength": "9", "id": "id_cep",
            }),
            "logradouro": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Rua, Avenida...",
                "id": "id_logradouro",
            }),
            "numero": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Nº",
                "id": "id_numero",
            }),
            "bairro": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Bairro",
                "id": "id_bairro",
            }),
            "cidade": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Cidade",
                "id": "id_cidade",
            }),
            "uf": forms.Select(attrs={
                "class": "form-select", "id": "id_uf",
            }),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get("cnpj", "")
        cnpj_limpo = re.sub(r"\D", "", cnpj)
        validado = validar_cnpj(cnpj_limpo)
        return f"{validado[:2]}.{validado[2:5]}.{validado[5:8]}/{validado[8:12]}-{validado[12:]}"

    def clean_cep(self):
        cep = re.sub(r"\D", "", self.cleaned_data.get("cep", ""))
        if cep and len(cep) != 8:
            raise forms.ValidationError("CEP inválido.")
        if cep:
            return f"{cep[:5]}-{cep[5:]}"
        return ""
