from django.db import migrations, models
import django.core.validators
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ("produtos", "0001_initial"),
    ]

    operations = [
        migrations.AddField(model_name="produto", name="ncm",
            field=models.CharField(blank=True, max_length=10, verbose_name="NCM")),
        migrations.AddField(model_name="produto", name="cest",
            field=models.CharField(blank=True, max_length=9, verbose_name="CEST")),
        migrations.AddField(model_name="produto", name="origem",
            field=models.CharField(choices=[("0","0 – Nacional"),("1","1 – Estrangeira (importação direta)"),("2","2 – Estrangeira (adquirida no mercado interno)"),("3","3 – Nacional com conteúdo estrangeiro > 40%"),("4","4 – Nacional, produção conforme processos básicos"),("5","5 – Nacional com conteúdo estrangeiro ≤ 40%"),("6","6 – Estrangeira (importação direta) sem similar"),("7","7 – Estrangeira (mercado interno) sem similar"),("8","8 – Nacional, mercadoria ou bem com conteúdo importado > 70%")],
                default="0", max_length=1, verbose_name="Origem")),
        migrations.AddField(model_name="produto", name="aliquota_icms",
            field=models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal("0.00"))], verbose_name="Alíquota ICMS (%)")),
        migrations.AddField(model_name="produto", name="aliquota_ipi",
            field=models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal("0.00"))], verbose_name="Alíquota IPI (%)")),
        migrations.AddField(model_name="produto", name="aliquota_pis",
            field=models.DecimalField(decimal_places=2, default=Decimal("0.65"), max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal("0.00"))], verbose_name="Alíquota PIS (%)")),
        migrations.AddField(model_name="produto", name="aliquota_cofins",
            field=models.DecimalField(decimal_places=2, default=Decimal("3.00"), max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal("0.00"))], verbose_name="Alíquota COFINS (%)")),
    ]
