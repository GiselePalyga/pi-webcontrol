from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal

from apps.notas.models import NotaFiscal
from apps.financeiro.models import Pagamento


@login_required
def dashboard(request):
    hoje = timezone.now().date()

    # Atualiza status de notas vencidas
    notas_vencidas_pendentes = NotaFiscal.objects.filter(
        status=NotaFiscal.STATUS_PENDENTE,
        data_vencimento__lt=hoje,
    )
    for nota in notas_vencidas_pendentes:
        nota.status = NotaFiscal.STATUS_VENCIDA
        nota.save(update_fields=["status"])

    total_pendente = sum(
        n.saldo_devedor for n in NotaFiscal.objects.filter(status=NotaFiscal.STATUS_PENDENTE)
    )
    total_vencido = sum(
        n.saldo_devedor for n in NotaFiscal.objects.filter(status=NotaFiscal.STATUS_VENCIDA)
    )
    total_pago_mes = Pagamento.objects.filter(
        data_pagamento__year=hoje.year,
        data_pagamento__month=hoje.month,
    ).aggregate(total=Sum("valor_pago"))["total"] or Decimal("0.00")

    count_pendente = NotaFiscal.objects.filter(status=NotaFiscal.STATUS_PENDENTE).count()
    count_vencida = NotaFiscal.objects.filter(status=NotaFiscal.STATUS_VENCIDA).count()
    count_paga = NotaFiscal.objects.filter(status=NotaFiscal.STATUS_PAGA).count()

    proximos_vencimentos = NotaFiscal.objects.filter(
        status__in=[NotaFiscal.STATUS_PENDENTE, NotaFiscal.STATUS_VENCIDA],
    ).select_related("fornecedor").order_by("data_vencimento")[:5]

    ultimas_notas = NotaFiscal.objects.select_related("fornecedor").order_by("-criado_em")[:5]

    context = {
        "total_pendente": total_pendente,
        "total_vencido": total_vencido,
        "total_pago_mes": total_pago_mes,
        "count_pendente": count_pendente,
        "count_vencida": count_vencida,
        "count_paga": count_paga,
        "proximos_vencimentos": proximos_vencimentos,
        "ultimas_notas": ultimas_notas,
        "hoje": hoje,
    }
    return render(request, "dashboard/index.html", context)
