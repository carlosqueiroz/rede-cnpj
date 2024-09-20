from bs4 import BeautifulSoup
import requests, os, sys, time, glob, parfive

url_dados_abertos = 'http://200.152.38.155/CNPJ/dados_abertos_cnpj/'

pasta_zip = r"dados-publicos-zip"  # Local dos arquivos zipados da Receita
pasta_cnpj = 'dados-publicos'

def requisitos():
    # Cria as pastas, se não existirem
    if not os.path.isdir(pasta_cnpj):
        os.mkdir(pasta_cnpj)
    if not os.path.isdir(pasta_zip):
        os.mkdir(pasta_zip)
        
    arquivos_existentes = list(glob.glob(pasta_cnpj +'/*.*')) + list(glob.glob(pasta_zip + '/*.*'))
    if len(arquivos_existentes):
        print('Apagando arquivos antigos...')
        for arq in arquivos_existentes:
            os.remove(arq)

requisitos()

print(time.asctime(), f'Início de {sys.argv[0]}:')

soup_pagina_dados_abertos = BeautifulSoup(requests.get(url_dados_abertos).text, features="lxml")
try:
    ultima_referencia = sorted([link.get('href') for link in soup_pagina_dados_abertos.find_all('a') if link.get('href').startswith('20')])[-1]
except:
    print('Não encontrou pastas em ' + url_dados_abertos)
    sys.exit(1)

url = url_dados_abertos + ultima_referencia
soup = BeautifulSoup(requests.get(url).text, features="lxml")
lista = []
print('Relação de Arquivos em ' + url)
for link in soup.find_all('a'):
    if str(link.get('href')).endswith('.zip'): 
        cam = link.get('href')
        if not cam.startswith('http'):
            lista.append(url+cam)
        else:
            lista.append(cam)

print(time.asctime(), 'Início do Download dos arquivos...')

downloader = parfive.Downloader()
for url in lista:
    downloader.enqueue_file(url, path=pasta_zip, filename=os.path.split(url)[1])
downloader.download()

print('\n\n'+ time.asctime(), f' Finalizou {sys.argv[0]}!!!')
print(f"Baixou {len(glob.glob(os.path.join(pasta_zip,'*.zip')))} arquivos.")
