# ML_Finance

## Descrição do Projeto

O **ML_Finance** é uma aplicação Flask projetada para realizar previsões de preços de fechamento de ações utilizando um modelo de rede neural LSTM (Long Short-Term Memory). A aplicação é capaz de obter dados financeiros históricos de ações, treinar um modelo com esses dados e prever valores futuros.

O projeto está estruturado para ser facilmente implantado em plataformas como o [Railway](https://railway.app) utilizando **Docker** e **nixpacks.toml**.

---

## Estrutura do Projeto

```
ml_finance/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── utils.py
│   └── config.py
├── run.py
├── requirements.txt
├── nixpacks.toml
└── Dockerfile
```

### Descrição dos Arquivos

- **`app/__init__.py`**: Configuração inicial da aplicação Flask e registro das rotas.
- **`app/routes.py`**: Define as rotas e endpoints da API.
- **`app/utils.py`**: Contém a lógica de predição de preços utilizando LSTM.
- **`app/config.py`**: Configuração da chave secreta para a aplicação Flask.
- **`run.py`**: Ponto de entrada principal para rodar a aplicação.
- **`requirements.txt`**: Lista de dependências do projeto.
- **`nixpacks.toml`**: Configuração para deploy no Railway.
- **`Dockerfile`**: Configuração para containerização da aplicação.

---

## Configuração e Execução Local

### 1. Clonar o Repositório

```bash
git clone https://github.com/diogobho/API_FINANCE_ML.git
cd API_FINANCE_ML
```

### 2. Configurar o Ambiente Virtual

Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instalar Dependências

Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

### 4. Executar a Aplicação Localmente

Inicie o servidor Flask:

```bash
python run.py
```

A aplicação estará disponível em `http://127.0.0.1:5000`.

---

## Uso da API

### Endpoint Principal

**URL:** `/<symbol>/<start_date>/<end_date>/<future_days>`

**Método HTTP:** `GET`

### Parâmetros

| Nome           | Tipo   | Descrição                                      |
|----------------|--------|--------------------------------------------------|
| `symbol`       | string | Símbolo da ação (e.g., `AAPL` para Apple).        |
| `start_date`   | string | Data de início no formato `YYYY-MM-DD`.           |
| `end_date`     | string | Data final no formato `YYYY-MM-DD`.             |
| `future_days`  | int    | Número de dias futuros para prever.              |

### Exemplo de Chamada

```bash
curl "https://apifinanceml-production.up.railway.app/AAPL/2023-01-01/2023-12-01/5"
```

### Exemplo de Resposta

```json
[
    {"Date": "2023-12-02", "Predicted Close": 175.12},
    {"Date": "2023-12-03", "Predicted Close": 176.45},
    {"Date": "2023-12-04", "Predicted Close": 177.89},
    {"Date": "2023-12-05", "Predicted Close": 178.34},
    {"Date": "2023-12-06", "Predicted Close": 179.12}
]
```

---

## Deploy no Railway

### Arquivo `nixpacks.toml`

```toml
[start]
cmd = "gunicorn run:app"
```

### Dockerfile

```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "run:app"]
```

### Passos para Deploy

1. Inicialize o repositório no Railway:

   ```bash
   railway init
   ```

2. Suba o projeto:

   ```bash
   railway up
   ```

3. Gere o domínio da aplicação:

   - Acesse **Networking** nas configurações do Railway.
   - Clique em **Generate Domain** para criar o URL público.

---

## Tecnologias Utilizadas

- **Flask**: Framework para criação de APIs.
- **TensorFlow/Keras**: Construção de modelos de redes neurais.
- **yFinance**: Extração de dados financeiros.
- **Docker**: Containerização para ambientes consistentes.
- **Railway**: Plataforma de deploy.

---

## Autores

- Diogo Bortolozo
- Reryson Farinha

---


