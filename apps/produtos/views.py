from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Produto
from .forms import ProdutoForm


@login_required
def lista(request):
    busca = request.GET.get("busca", "").strip()
    ativo = request.GET.get("ativo", "")
    qs = Produto.objects.all()
    if busca:
        qs = qs.filter(Q(nome__icontains=busca))
    if ativo == "1":
        qs = qs.filter(ativo=True)
    elif ativo == "0":
        qs = qs.filter(ativo=False)
    return render(request, "produtos/lista.html", {"produtos": qs, "busca": busca, "ativo": ativo})


@login_required
def novo(request):
    form = ProdutoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Produto cadastrado com sucesso!")
        return redirect("produtos:lista")
    return render(request, "produtos/form.html", {"form": form, "titulo": "Novo Produto"})


@login_required
def editar(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    form = ProdutoForm(request.POST or None, instance=produto)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Produto atualizado com sucesso!")
        return redirect("produtos:lista")
    return render(request, "produtos/form.html", {"form": form, "titulo": "Editar Produto", "produto": produto})


@login_required
def produto_json(request, pk):
    produto = get_object_or_404(Produto, pk=pk, ativo=True)
    return JsonResponse({
        "nome": produto.nome,
        "preco_venda": str(produto.preco_venda),
        "unidade_medida": produto.get_unidade_medida_display(),
    })


@login_required
def toggle_ativo(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    produto.ativo = not produto.ativo
    produto.save(update_fields=["ativo"])
    status = "ativado" if produto.ativo else "inativado"
    messages.success(request, f"Produto {status} com sucesso!")
    return redirect("produtos:lista")
