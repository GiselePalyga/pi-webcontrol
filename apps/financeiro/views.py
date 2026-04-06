from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.notas.models import NotaFiscal
from .models import Pagamento
from .forms import PagamentoForm


@login_required
def registrar_pagamento(request, nota_pk):
    nota = get_object_or_404(NotaFiscal, pk=nota_pk)
    if request.method == "POST":
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pagamento = form.save(commit=False)
            pagamento.nota_fiscal = nota
            try:
                pagamento.full_clean()
                pagamento.save()
                messages.success(request, f"Pagamento de R$ {pagamento.valor_pago} registrado!")
            except Exception as e:
                messages.error(request, str(e))
        else:
            for field, erros in form.errors.items():
                for erro in erros:
                    messages.error(request, f"{erro}")
    return redirect("notas:detalhe", pk=nota_pk)


@login_required
def excluir_pagamento(request, pk):
    pagamento = get_object_or_404(Pagamento, pk=pk)
    nota_pk = pagamento.nota_fiscal_id
    if request.method == "POST":
        nota = pagamento.nota_fiscal
        pagamento.delete()
        nota.atualizar_status()
        messages.success(request, "Pagamento excluído com sucesso!")
    return redirect("notas:detalhe", pk=nota_pk)
