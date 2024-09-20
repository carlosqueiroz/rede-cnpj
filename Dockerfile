# Use uma imagem Python base
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia todos os arquivos do projeto para o container
COPY . /app

# Instala as dependências do 'rede'
RUN pip install --upgrade pip && pip install -r rede/requirements.txt

# Instala as dependências do 'rede_cria_tabelas'
RUN pip install -r rede_cria_tabelas/requirements.txt

# Baixa os arquivos zip do site de Dados Abertos
RUN python rede_cria_tabelas/dados_cnpj_baixa.py

# Cria a base de empresas (cnpj.db)
RUN python rede_cria_tabelas/dados_cnpj_para_sqlite.py

# Cria a tabela de vínculos (rede.db)
RUN python rede_cria_tabelas/rede_cria_tabela_rede.db.py

# Cria a tabela de endereços, emails e telefones (cnpj_links_ete.db)
RUN python rede_cria_tabelas/rede_cria_tabela_cnpj_links_ete.py

# Comando para manter o container ativo
CMD ["tail", "-f", "/dev/null"]
