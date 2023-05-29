from django.shortcuts import render
from .models import Produto 


def pesquisar(request):
    return render(request, 'produtos/pesquisa.html')

def exibir_resultados(request):
    nome_produto = request.POST.get('produto')
    print(nome_produto)
    dados = {
        "dados": Produto.objects.filter(nome__icontains=nome_produto).order_by('preco')  
    }
    return render(request,'protudos/resultado_pesquisa.html',dados)
