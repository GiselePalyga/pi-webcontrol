from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal

from apps.notas.models import NotaFiscal


class Pagamento(models.Model):
    FORMA_CHOICES = [
        ("dinheiro", "Dinheiro"),
        ("pix", "PIX"),
        ("boleto", "Boleto"),
        ("transferencia", "Transferência Bancária"),
        ("cartao_debito", "Cartão de Débito"),
        ("cartao_credito", "Cartão de Crédito"),
        ("cheque", "Cheque"),
    ]

    nota_fiscal = models.ForeignKey(
        NotaFiscal,
        on_delete=models.CASCADE,
        verbose_name="Nota Fiscal",
        related_name="pagamentos",
    )
    data_pagamento = models.DateField("Data de Pagamento")
    valor_pago = models.DecimalField(
        "Valor Pago",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    forma_pagamento = models.CharField(
        "Forma de Pagamento", max_length=20, choices=FORMA_CHOICES, default="pix"
    )
    observacoes = models.TextField("Observações", blank=True)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"
        ordering = ["-data_pagamento"]

    def __str__(self):
        return f"Pgto R$ {self.valor_pago} - {self.nota_fiscal}"

    def clean(self):
        if self.valor_pago and self.nota_fiscal_id:
            saldo = self.nota_fiscal.saldo_devedor
            # Se for edição, soma o valor atual de volta antes de checar
            if self.pk:
                saldo += Pagamento.objects.get(pk=self.pk).valor_pago
            if self.valor_pago > saldo:
                raise ValidationError(
                    {"valor_pago": f"O valor pago (R$ {self.valor_pago}) excede o saldo devedor (R$ {saldo:.2f})."}
                )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.nota_fiscal.atualizar_status()
