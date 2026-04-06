from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Fornecedor
from .forms import FornecedorForm


@login_required
def lista(request):
    busca = request.GET.get("busca", "").strip()
    ativo = request.GET.get("ativo", "")
    qs = Fornecedor.objects.all()
    if busca:
        qs = qs.filter(
            Q(nome_fantasia__icontains=busca)
            | Q(razao_social__icontains=busca)
            | Q(cnpj__icontains=busca)
            | Q(cidade__icontains=busca)
        )
    if ativo == "1":
        qs = qs.filter(ativo=True)
    elif ativo == "0":
        qs = qs.filter(ativo=False)
    return render(request, "fornecedores/lista.html", {"fornecedores": qs, "busca": busca, "ativo": ativo})


@login_required
def novo(request):
    form = FornecedorForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Fornecedor cadastrado com sucesso!")
        return redirect("fornecedores:lista")
    return render(request, "fornecedores/form.html", {"form": form, "titulo": "Novo Fornecedor"})


@login_required
def editar(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    form = FornecedorForm(request.POST or None, instance=fornecedor)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Fornecedor atualizado com sucesso!")
        return redirect("fornecedores:lista")
    return render(request, "fornecedores/form.html", {"form": form, "titulo": "Editar Fornecedor", "fornecedor": fornecedor})


@login_required
def toggle_ativo(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    fornecedor.ativo = not fornecedor.ativo
    fornecedor.save(update_fields=["ativo"])
    status = "ativado" if fornecedor.ativo else "inativado"
    messages.success(request, f"Fornecedor {status} com sucesso!")
    return redirect("fornecedores:lista")
