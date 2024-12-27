

!pip install langchain
!pip install langchain-groq
!pip install langchain-community
!pip install youtube_transcript_api
!pip install pypdf

import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

api_key = 'chave_groq'
os.environ['GROQ_API_KEY'] = api_key

chat = ChatGroq(model = 'llama-3.3-70b-versatile')

def resposta_bot(mensagens, documento):
  mensagem_system = '''Você é um assistente amigável
  Você utiliza as seguintes informações para formular as suas respostas: {informacoes}'''
  mensagens_modelo = [('system',mensagem_system)]
  mensagens_modelo += mensagens
  template = ChatPromptTemplate.from_messages(mensagens_modelo)
  chain = template | chat
  return chain.invoke({'informacoes':documento}).content

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders import PyPDFLoader

def carrega_site():
  url_site = input('Digite url site')
  loader = WebBaseLoader(url_site)
  lista_documentos = loader.load()
  documento = ''
  for doc in lista_documentos:
    documento = documento + doc.page_content
  return documento

def carrega_pdf():
  caminho = 'https://media.licdn.com/dms/document/media/v2/D4D1FAQEdbDm9WR0klQ/feedshare-document-pdf-analyzed/B4DZPf2PxjHMAY-/0/1734627365068?e=1736380800&v=beta&t=kmhBXXKBjgQrv2M8vFoKFUEnMeZL3_DpUG2zasiAyYI'
  loader = PyPDFLoader(caminho)
  lista_documentos = loader.load()
  documento = ''
  for doc in lista_documentos:
    documento = documento + doc.page_content
  return documento


def carrega_youtube():
  url_youtube = input('Digite url do video')
  loader = YoutubeLoader.from_youtube_url(url_youtube,language=['pt'])
  lista_documnetos = loader.load()
  documento = ''
  for doc in lista_documentos:
    documento = documento + doc.page_content
  return documento

print('Bem-vindo ao bot')

texto_selecao = ''' Digite 1 se você quiser conversar com um site
Digite 2 se você quiser conversar com um pdf
Digite 3 se você quiser conversar com um video youtube
'''
while True:
  selecao = input(texto_selecao)
  if selecao == '1':
    print('site')
    documento = carrega_site()
    break
  if selecao == '2':
    print('pdf')
    documento = carrega_pdf()
    break
  if selecao == '3':
    print('youtube')
    documento = carrega_youtube()
    break
  print('Digite valor entre 1 e 3')

mensagens = []

while True:
  pergunta = input('Usuario: ')
  if pergunta.lower() == 'x' :
    break
  mensagens.append(('user', pergunta))
  resposta = resposta_bot(mensagens, documento)
  mensagens.append(('assistant', resposta))
  print(f'Bot: {resposta}')
print('muito obrigado por usar o bot')
print(mensagens)