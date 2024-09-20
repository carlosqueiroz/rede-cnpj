# Use uma imagem Python base
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de dependências e código para o container
COPY . /app

# Instala as dependências do projeto
RUN pip install --upgrade pip && pip install -r requirements.txt

# Baixa os arquivos zip do site de Dados Abertos
RUN python dados_cnpj_baixa.py

# Cria a base de empresas (cnpj.db)
RUN python dados_cnpj_para_sqlite.py

# Cria a tabela de vínculos (rede.db)
RUN python rede_cria_tabela_rede.db.py

# Cria a tabela de endereços, emails e telefones (cnpj_links_ete.db)
RUN python rede_cria_tabela_cnpj_links_ete.py

# Comando de entrada para manter o container rodando
CMD ["tail", "-f", "/dev/null"]
