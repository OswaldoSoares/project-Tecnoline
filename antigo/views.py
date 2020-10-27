from django.shortcuts import render
from .models import Servico, Pessoa, Servicoitem

def index_servico(request):
    servico = Servico.objects.filter(status='ABERTA')
    os = {}
    for item in servico:
        os[item.idservico] = {}
        cliente_queryset = Pessoa.objects.filter(idpessoa=item.idcadastro)
        cliente = None
        if cliente_queryset:
            cliente = list(cliente_queryset.values_list('apelido').values())[0]
        nome = None
        if cliente:
            nome = cliente.get('apelido')
        os[item.idservico]['Cliente'] = nome
        os[item.idservico]['Solicitante'] = item.solicitante
        os[item.idservico]['Obra'] = item.obra
        os[item.idservico]['Itens'] = {}
        itens_servico_queryset = Servicoitem.objects.filter(idservico=item.idservico)
        itens_servico = list(itens_servico_queryset.values_list().values())
        for x in itens_servico:
            os[x.idservicoitem]['Originais'] = 1
            os[x.idservicoitem]['Copias'] = 2
            os[x.idservicoitem]['Valor'] = 3
            os[x.idservicoitem]['Tmanho'] = 4
    print(os)
    return render(request, 'antigo/index.html', {'os': os})
