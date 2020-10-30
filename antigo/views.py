from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape

from .models import Servico, Pessoa, Servicoitem, Produto

def index_servico(request):
    servico = Servico.objects.filter(status='ENTREGAR')
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
        os[item.idservico]['idservico'] = item.idservico
        os[item.idservico]['Cliente'] = nome
        os[item.idservico]['Solicitante'] = item.solicitante
        os[item.idservico]['Obra'] = item.obra
        os[item.idservico]['Itens'] = {}
        # itens_servico_queryset = Servicoitem.objects.filter(idservico=item.idservico)
        # itens_servico = list(itens_servico_queryset.values_list().values())
        # for x in itens_servico:
        #     os[x.idservicoitem]['Originais'] = 1
        #     os[x.idservicoitem]['Copias'] = 2
        #     os[x.idservicoitem]['Valor'] = 3
        #     os[x.idservicoitem]['Tmanho'] = 4

    return render(request, 'antigo/index.html', {'os': os})


def convertemp(mm):
    """
    Converte milimetros em pontos. Usado na criação de PDF (ex. Relatórios)
    :param mm: float
    :return: float
    """
    return mm / 0.352777


def imprime_servico(request, idservico):
    """
    Função que gera o PDF da OS. Impressão em uma folha A4 em posição landscape, imprime 2 vias na mesma folha,
    a variável posx que possibilita a impressão da 2 via ao lado. Utilização da biblioteca ReportLab.
    :param request: request
    :param idservico: integer
    :return:
    """
    servico = Servico.objects.get(idservico=idservico)
    cliente = Pessoa.objects.get(idpessoa=servico.idcadastro)
    qs_servico_item = Servicoitem.objects.filter(idservico=idservico)
    servico_item = list(qs_servico_item.values())
    for index, item in enumerate(servico_item):
        idproduto = servico_item[index]['idproduto']
        produto = Produto.objects.get(idproduto=idproduto)
        servico_item[index]['idproduto'] = produto.descricao
        servico_item[index]['codigo'] = produto.codigo
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=landscape(A4))
    posx = 0
    for n in range(2):
        pdf.roundRect(convertemp(5+posx), convertemp(5), convertemp(138.5), convertemp(200), 10)
        pdf.drawImage('website/static/website/img/tecnoline_logo.jpg', convertemp(11+posx), convertemp(188), convertemp(
            55.21), convertemp(15))
        pdf.roundRect(convertemp(101+posx), convertemp(190), convertemp(30), convertemp(10), 10)
        pdf.setFont("Times-Bold", 12)
        pdf.drawString(convertemp(106.5+posx), convertemp(193.5), 'OS: ' + str(servico.idservico))
        pdf.setFont("Times-Bold", 10)
        pdf.drawCentredString(convertemp(74+posx), convertemp(184), 'Rua Pe Benedito de Camargo, 385 - CEP 03604-010 - '
                                                                 'São Paulo - SP')
        pdf.drawCentredString(convertemp(74+posx), convertemp(180), '(11) 2647-1200 - Whatsapp (11) 94233-8804')
        pdf.drawCentredString(convertemp(74+posx), convertemp(176), 'tecnoline@uol.com.br')
        pdf.line(convertemp(5+posx), convertemp(175), convertemp(143.5+posx), convertemp(175))
        pdf.line(convertemp(5+posx), convertemp(165), convertemp(143.5+posx), convertemp(165))
        pdf.setFont("Times-Bold", 12)
        pdf.setFillColor(HexColor("#c1c1c1"))
        pdf.setStrokeColor(HexColor("#c1c1c1"))
        pdf.rect(convertemp(5.5+posx), convertemp(170),convertemp(67.75), convertemp(4.5), fill=1, stroke=1)
        pdf.rect(convertemp(74.5+posx), convertemp(170),convertemp(68.25), convertemp(4.5), fill=1, stroke=1)
        pdf.setFillColor(HexColor("#000000"))
        pdf.setStrokeColor(HexColor("#000000"))
        pdf.drawCentredString(convertemp(39.5+posx), convertemp(171), cliente.apelido)
        pdf.drawCentredString(convertemp(108.5+posx), convertemp(171), servico.solicitante)
        pdf.setFont("Times-Roman", 9)
        pdf.drawString(convertemp(24+posx), convertemp(166), 'Descrição')
        # pdf.drawCentredString(convertemp(50.5), convertemp(166), 'Código')
        pdf.drawRightString(convertemp(73+posx), convertemp(166), 'Originais')
        pdf.drawRightString(convertemp(85+posx), convertemp(166), 'Cópias')
        pdf.drawRightString(convertemp(96+posx), convertemp(166), 'Medida')
        pdf.drawRightString(convertemp(107+posx), convertemp(166), 'Quant.')
        pdf.drawRightString(convertemp(120+posx), convertemp(166), 'Valor')
        pdf.drawRightString(convertemp(138+posx), convertemp(166), 'Total')
        linha = 166
        total = 0
        for x in servico_item:
            print(x)
            pdf.drawString(convertemp(6+posx), convertemp(linha-4), x.get('idproduto'))
            # pdf.drawCentredString(convertemp(50.5), convertemp(linha-4), x.get('codigo'))
            pdf.drawRightString(convertemp(69+posx), convertemp(linha-4), str(x.get('originais')))
            pdf.drawRightString(convertemp(83+posx), convertemp(linha-4), str(x.get('copias')))
            pdf.drawRightString(convertemp(95+posx), convertemp(linha-4), str(x.get('tamanho')))
            pdf.drawRightString(convertemp(104+posx), convertemp(linha-4), str(x.get('originais') * x.get('copias')))
            pdf.drawRightString(convertemp(123+posx), convertemp(linha-4), 'R$ {:.2f}'.format(x.get(
                'valor')).replace('.',','))
            pdf.drawRightString(convertemp(142+posx), convertemp(linha-4), 'R$ {:.2f}'.format(x.get('originais') *
                x.get('copias') * x.get('tamanho') * x.get('valor')).replace('.',','))
            total += x.get('originais') * x.get('copias') * x.get('tamanho') * x.get('valor')
            pdf.line(convertemp(5+posx), convertemp(linha-5), convertemp(143.5+posx), convertemp(linha-5))
            linha -= 4
        pdf.setFillColor(HexColor("#c1c1c1"))
        pdf.setStrokeColor(HexColor("#c1c1c1"))
        pdf.rect(convertemp(5.5+posx), convertemp(linha-7.5),convertemp(137.5), convertemp(6), fill=1, stroke=1)
        pdf.setFillColor(HexColor("#000000"))
        pdf.setStrokeColor(HexColor("#000000"))
        pdf.setFont("Times-Bold", 10)
        pdf.drawString(convertemp(6+posx), convertemp(linha-6), 'Data: {:%d/%m/%Y}'.format(servico.diaservico))
        pdf.drawRightString(convertemp(142+posx), convertemp(linha-6), 'R$ {:.2f}'.format(total).replace('.',','))
        pdf.line(convertemp(5+posx), convertemp(linha-8), convertemp(143.5+posx), convertemp(linha-8))
        pdf.line(convertemp(5+posx), convertemp(55), convertemp(143.5+posx), convertemp(55))
        pdf.drawString(convertemp(7+posx), convertemp(51), 'Observações:')
        pdf.drawString(convertemp(7.5+posx), convertemp(46), servico.obs)
        pdf.rect(convertemp(7+posx), convertemp(34), convertemp(134.5), convertemp(15))
        pdf.drawString(convertemp(7+posx), convertemp(29), 'Obra')
        pdf.drawString(convertemp(7+posx), convertemp(24), servico.obra)
        pdf.drawString(convertemp(7+posx), convertemp(16), 'Recebemos os originais e as cópias em perfeito estado.')
        pdf.drawString(convertemp(7+posx), convertemp(7), 'Name:________________________________')
        pdf.drawString(convertemp(75+posx), convertemp(7), 'ASS:________________________________')
        posx += 148.5
    pdf.setTitle('OS' + str(servico.idservico) + '.pdf')
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
