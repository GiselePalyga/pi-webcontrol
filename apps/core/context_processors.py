from django.utils import timezone
from datetime import timedelta


def notificacoes(request):
    if not request.user.is_authenticated:
        return {"notificacoes": [], "count_notif": 0}

    from apps.notas.models import NotaFiscal

    hoje = timezone.now().date()
    em_7_dias = hoje + timedelta(days=7)

    vencidas = list(
        NotaFiscal.objects.filter(status=NotaFiscal.STATUS_VENCIDA)
        .select_related("fornecedor")
        .order_by("data_vencimento")[:10]
    )
    a_vencer = list(
        NotaFiscal.objects.filter(
            status=NotaFiscal.STATUS_PENDENTE,
            data_vencimento__gte=hoje,
            data_vencimento__lte=em_7_dias,
        )
        .select_related("fornecedor")
        .order_by("data_vencimento")[:10]
    )

    notifs = []
    for n in vencidas:
        notifs.append({"nota": n, "tipo": "vencida", "dias": (hoje - n.data_vencimento).days})
    for n in a_vencer:
        dias = (n.data_vencimento - hoje).days
        notifs.append({"nota": n, "tipo": "a_vencer", "dias": dias})

    return {"notificacoes": notifs, "count_notif": len(notifs)}
