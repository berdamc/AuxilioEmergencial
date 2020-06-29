import csv
import os
from reportlab.pdfgen import canvas

def GeneratePDF(lista,nome_pdf,cidadeUF):
    try:
        pdf = canvas.Canvas(nome_pdf)
        pdf.setTitle(cidadeUF)
        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawCentredString(300, 800, ' Lista do Auxílio Emergencial - Dados do Portal da Transparência - Abril/2020 ')
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawCentredString(300, 770, '  Denúncias e consultas devem ser feitas no Portal da Transparência   ')
        pdf.drawCentredString(300, 750, ' Acesse http://gg.gg/portaltransparencia4, altere os filtros e consulte  ')
        pdf.drawCentredString(300, 730, ' Para outras cidades/meses/README acesse http://gg.gg/informacoesauxilio ')
        pdf.drawCentredString(300, 700, 'Beneficiários de ' + cidadeUF)
        pdf.setFont("Helvetica", 12)

        pdf.drawString(50, 670, 'Name')
        pdf.drawCentredString(400,670, 'CPF')
        pdf.drawRightString(550, 670, 'Valor')
        pdf.setFillColorRGB(0, 0, 0)

        y = 670
        for UF,CodMunicipio,NomeMunicipio,CPF,NomeBeneficiado,Valor in lista:
            y -= 20

            pdf.drawString(50, y, NomeBeneficiado)
            pdf.drawCentredString(400, y, CPF)
            pdf.drawRightString(550, y, Valor)

            if y < 50:
                pdf.showPage()
                y = 800

        pdf.save()
    except:
        print('Erro ao gerar {}.pdf'.format(nome_pdf))

dados = []
pastainicial = 'maio/'

if not os.path.isdir(pastainicial):
    os.mkdir(pastainicial)

with open('dados05.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    MunicipioAnterior = 'PessoasSemMunicipio'
    UFAnterior = 'PessoasSemEstado'
    for row in csv_reader:
        if line_count > 0:
            if row:
                UF = row[1]
                CodMunicipio = row[2]
                NomeMunicipio = row[3]
                CPF = row[5]
                NomeBeneficiado = row[6]
                Valor = row[13]

                if UF == '': #Existem beneficiados sem estado no arquivo de Abril
                   UF = 'PessoasSemEstado'

                if NomeMunicipio == '':
                   NomeMunicipio = 'PessoasSemMunicipio'

                if not os.path.isdir(pastainicial + UF + '/'):
                   os.mkdir(pastainicial + UF + '/')

                if NomeMunicipio+'-'+UF != MunicipioAnterior+'-'+UFAnterior:

                    if len(dados) > 0:
                       print("Gerando arquivo de",MunicipioAnterior+'-'+UFAnterior)
                       GeneratePDF(dados,pastainicial+UFAnterior+'/'+MunicipioAnterior+'.pdf',MunicipioAnterior+'-'+UFAnterior)

                    MunicipioAnterior = NomeMunicipio
                    UFAnterior = UF

                    dados = []

                dados.append([UF,CodMunicipio,NomeMunicipio,CPF,NomeBeneficiado,Valor])

        print("Processando linha",line_count)
        line_count = line_count + 1

if len(dados) > 0:  # se for fim de arquivo, existem maio armazenados na memória que devem ser salvos
   print("Gerando arquivo de",MunicipioAnterior+'-'+UFAnterior)
GeneratePDF(dados, pastainicial + UFAnterior + '/' + MunicipioAnterior + '.pdf', MunicipioAnterior + '-' + UFAnterior)


print("Processamento finalizado !!!")