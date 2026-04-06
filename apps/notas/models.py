from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.utils import timezone

from apps.fornecedores.models import Fornecedor
from apps.produtos.models import Produto


class NotaFiscal(models.Model):
    STATUS_PENDENTE = "pendente"
    STATUS_PAGA = "paga"
    STATUS_VENCIDA = "vencida"
    STATUS_CANCELADA = "cancelada"

    STATUS_CHOICES = [
        (STATUS_PENDENTE, "Pendente"),
        (STATUS_PAGA, "Paga"),
        (STATUS_VENCIDA, "Vencida"),
        (STATUS_CANCELADA, "Cancelada"),
    ]

    numero = models.CharField("Número", max_length=20)
    serie = models.CharField("Série", max_length=10, default="1")
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.PROTECT,
        verbose_name="Fornecedor",
        related_name="notas_fiscais",
    )
    data_emissao = models.DateField("Data de Emissão")
    data_vencimento = models.DateField("Data de Vencimento")
    valor_total = models.DecimalField(
        "Valor Total",
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    status = models.CharField(
        "Status", max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDENTE
    )
    observacoes = models.TextField("Observações", blank=True)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Nota Fiscal"
        verbose_name_plural = "Notas Fiscais"
        ordering = ["-data_emissao"]
        unique_together = [["numero", "serie", "fornecedor"]]

    def __str__(self):
        return f"NF {self.numero}/{self.serie} - {self.fornecedor.nome_fantasia}"

    def clean(self):
        if self.data_vencimento and self.data_emissao:
            if self.data_vencimento < self.data_emissao:
                raise ValidationError(
                    {"data_vencimento": "A data de vencimento não pode ser anterior à data de emissão."}
                )

    @property
    def total_pago(self):
        return self.pagamentos.aggregate(
            total=models.Sum("valor_pago")
        )["total"] or Decimal("0.00")

    @property
    def saldo_devedor(self):
        return self.valor_total - self.total_pago

    @property
    def esta_vencida(self):
        return (
            self.status == self.STATUS_PENDENTE
            and self.data_vencimento < timezone.now().date()
        )

    def atualizar_status(self):
        """Atualiza o status com base nos pagamentos realizados."""
        if self.status == self.STATUS_CANCELADA:
            return
        if self.saldo_devedor <= Decimal("0.00"):
            self.status = self.STATUS_PAGA
        elif self.esta_vencida:
            self.status = self.STATUS_VENCIDA
        else:
            self.status = self.STATUS_PENDENTE
        self.save(update_fields=["status"])


class ItemNotaFiscal(models.Model):
    nota_fiscal = models.ForeignKey(
        NotaFiscal,
        on_delete=models.CASCADE,
        verbose_name="Nota Fiscal",
        related_name="itens",
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        verbose_name="Produto",
        related_name="itens_nota",
        null=True,
        blank=True,
    )
    descricao = models.CharField("Descrição", max_length=300)
    quantidade = models.DecimalField(
        "Quantidade",
        max_digits=10,
        decimal_places=3,
        validators=[MinValueValidator(Decimal("0.001"))],
    )
    valor_unitario = models.DecimalField(
        "Valor Unitário",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    valor_total = models.DecimalField(
        "Valor Total",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    class Meta:
        verbose_name = "Item da Nota Fiscal"
        verbose_name_plural = "Itens da Nota Fiscal"

    def __str__(self):
        return f"{self.descricao} ({self.quantidade})"

    def save(self, *args, **kwargs):
        self.valor_total = self.quantidade * self.valor_unitario
        super().save(*args, **kwargs)
