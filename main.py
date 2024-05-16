import google.generativeai as genai
import docx
from docx.shared import Pt

with open("Resources\API_KEY.txt","r") as apikey:
    API_KEY = apikey.read()

CV_base = docx.Document("Resources\CV Base ATS cod.docx")
style = CV_base.styles['Normal']
font = style.font
font.name='Times New Roman'
font.size=Pt(11)

descricao_vaga = input("Cole aqui a descrição da vaga\n")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

print('Coletando informações... Aguarde')
atividades_cv = {}
with open("Resources\CV bullets.txt") as f:
    for linha in f:
        variavel, descricao = linha.strip().split(':')
        atividades_cv[variavel] = descricao

print('Consultando com o Saga... Aguarde')
for chave in atividades_cv:
    parte = atividades_cv[chave]
    script = 'Responda somente com o texto alterado, sem cabeçalhos e sem formatação. Você vai agir como um consultor de recolocação e avaliar o CV para a vaga em questão. Seu trabalho será ajustar o texto para que os termos fiquem mais próximos da descrição da vaga, considerando que o CV será processado por um ATS. A descrição da vaga é:'
    script = script + descricao_vaga
    script = script + '\nO trecho a ser atualizado é: '
    script = script + parte
    response = model.generate_content(script)
#    print('script: ',script)
#    print('\nordem: ',chave,'\n resposta: ',response.text)
    atividades_cv[chave] = response.text
    print('Consultando, de novo, com o Saga... Aguarde, só mais um pouco')

print('Atualizando CV... Aguarde')
for paragrafo in CV_base.paragraphs:
    for chave in atividades_cv:
        checar = '{'+chave+'}'
        if checar in paragrafo.text:
            paragrafo.text = paragrafo.text.replace(checar,atividades_cv[chave])
            paragrafo.style = style


print('Salvando arquivo... Quase lá')
CV_base.save('CV.docx')
print('CV finalizado. Boa sorte')