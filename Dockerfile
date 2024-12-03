# Usar imagem oficial do Python
FROM python:3.11-slim

# Variável para rodar o Python em modo unbuffered
ENV PYTHONUNBUFFERED=1 

# Diretório de trabalho
WORKDIR /app

# Copiar código para o container
COPY . .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Comando para iniciar o servidor Gunicorn
CMD ["gunicorn", "run:app"]
