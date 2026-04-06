from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import NotaFiscal, ItemNotaFiscal
from .forms import NotaFiscalForm, ItemFormSet, NotaFiscalFiltroForm
from apps.financeiro.models import Pagamento
from apps.financeiro.forms import PagamentoForm


@login_required
def lista(request):
    form_filtro = NotaFiscalFiltroForm(request.GET or None)
    qs = NotaFiscal.objects.select_related("fornecedor").all()

    if form_filtro.is_valid():
        busca = form_filtro.cleaned_data.get("busca")
        status = form_filtro.cleaned_data.get("status")
        data_inicio = form_filtro.cleaned_data.get("data_inicio")
        data_fim = form_filtro.cleaned_data.get("data_fim")

        if busca:
            qs = qs.filter(
                Q(numero__icontains=busca)
                | Q(fornecedor__nome_fantasia__icontains=busca)
                | Q(fornecedor__cnpj__icontains=busca)
            )
        if status:
            qs = qs.filter(status=status)
        if data_inicio:
            qs = qs.filter(data_emissao__gte=data_inicio)
        if data_fim:
            qs = qs.filter(data_emissao__lte=data_fim)

    return render(request, "notas/lista.html", {"notas": qs, "form_filtro": form_filtro})


@login_required
def detalhe(request, pk):
    nota = get_object_or_404(NotaFiscal.objects.select_related("fornecedor"), pk=pk)
    itens = nota.itens.select_related("produto").all()
    pagamentos = nota.pagamentos.all()
    form_pgto = PagamentoForm()
    return render(request, "notas/detalhe.html", {
        "nota": nota,
        "itens": itens,
        "pagamentos": pagamentos,
        "form_pgto": form_pgto,
    })


@login_required
def novo(request):
    form = NotaFiscalForm(request.POST or None)
    formset = ItemFormSet(request.POST or None)

    if request.method == "POST":
        if form.is_valid() and formset.is_valid():
            nota = form.save()
            formset.instance = nota
            formset.save()
            nota.atualizar_status()
            messages.success(request, "Nota fiscal cadastrada com sucesso!")
            return redirect("notas:detalhe", pk=nota.pk)

    return render(request, "notas/form.html", {
        "form": form,
        "formset": formset,
        "titulo": "Nova Nota Fiscal",
    })


@login_required
def editar(request, pk):
    nota = get_object_or_404(NotaFiscal, pk=pk)
    form = NotaFiscalForm(request.POST or None, instance=nota)
    formset = ItemFormSet(request.POST or None, instance=nota)

    if request.method == "POST":
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            nota.atualizar_status()
            messages.success(request, "Nota fiscal atualizada com sucesso!")
            return redirect("notas:detalhe", pk=nota.pk)

    return render(request, "notas/form.html", {
        "form": form,
        "formset": formset,
        "titulo": "Editar Nota Fiscal",
        "nota": nota,
    })
