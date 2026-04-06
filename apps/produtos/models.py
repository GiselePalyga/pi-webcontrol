from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Produto(models.Model):
    UNIDADE_CHOICES = [
        ("UN", "Unidade"), ("KG", "Quilograma"), ("G", "Grama"),
        ("L", "Litro"), ("ML", "Mililitro"), ("M", "Metro"),
        ("M2", "Metro²"), ("M3", "Metro³"), ("CX", "Caixa"),
        ("PC", "Peça"), ("SC", "Saco"), ("FD", "Fardo"),
    ]

    ORIGEM_CHOICES = [
        ("0", "0 – Nacional"),
        ("1", "1 – Estrangeira (importação direta)"),
        ("2", "2 – Estrangeira (adquirida no mercado interno)"),
        ("3", "3 – Nacional com conteúdo estrangeiro > 40%"),
        ("4", "4 – Nacional, produção conforme processos básicos"),
        ("5", "5 – Nacional com conteúdo estrangeiro ≤ 40%"),
        ("6", "6 – Estrangeira (importação direta) sem similar"),
        ("7", "7 – Estrangeira (mercado interno) sem similar"),
        ("8", "8 – Nacional, mercadoria ou bem com conteúdo importado > 70%"),
    ]

    nome = models.CharField("Nome", max_length=200)
    unidade_medida = models.CharField("Unidade de Medida", max_length=3, choices=UNIDADE_CHOICES, default="UN")

    # Preços e estoque
    preco_custo = models.DecimalField("Preço de Custo", max_digits=10, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0.00"))])
    preco_venda = models.DecimalField("Preço de Venda", max_digits=10, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0.00"))])
    estoque_atual = models.DecimalField("Estoque Atual", max_digits=10, decimal_places=3, default=Decimal("0.000"), validators=[MinValueValidator(Decimal("0.000"))])
    estoque_minimo = models.DecimalField("Estoque Mínimo", max_digits=10, decimal_places=3, default=Decimal("0.000"), validators=[MinValueValidator(Decimal("0.000"))])

    # Dados fiscais
    ncm = models.CharField("NCM", max_length=10, blank=True, help_text="Nomenclatura Comum do Mercosul (ex: 7307.19.00)")
    cest = models.CharField("CEST", max_length=9, blank=True, help_text="Código Especificador da Substituição Tributária (ex: 10.001.00)")
    origem = models.CharField("Origem", max_length=1, choices=ORIGEM_CHOICES, default="0")
    aliquota_icms = models.DecimalField("Alíquota ICMS (%)", max_digits=5, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0.00"))])
    aliquota_ipi = models.DecimalField("Alíquota IPI (%)", max_digits=5, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0.00"))])
    aliquota_pis = models.DecimalField("Alíquota PIS (%)", max_digits=5, decimal_places=2, default=Decimal("0.65"), validators=[MinValueValidator(Decimal("0.00"))])
    aliquota_cofins = models.DecimalField("Alíquota COFINS (%)", max_digits=5, decimal_places=2, default=Decimal("3.00"), validators=[MinValueValidator(Decimal("0.00"))])

    ativo = models.BooleanField("Ativo", default=True)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} ({self.get_unidade_medida_display()})"

    @property
    def estoque_baixo(self):
        return self.estoque_atual <= self.estoque_minimo
