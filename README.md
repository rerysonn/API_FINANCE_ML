# Documentação do Código: Previsão de Preços de Ações com LSTM

Este código implementa um modelo de aprendizado profundo usando redes neurais LSTM para prever preços de fechamento futuros de ações. Ele utiliza dados financeiros históricos obtidos com a biblioteca `yfinance`.

---

## Bibliotecas Utilizadas

1. **`yfinance`**: Para obter dados históricos de preços de ações.
2. **`numpy`**: Para manipulação de arrays e cálculos matemáticos.
3. **`pandas`**: Para manipulação e formatação de dados tabulares.
4. **`sklearn.preprocessing.MinMaxScaler`**: Para normalização dos dados de entrada.
5. **`keras`**: Para construção, treinamento e avaliação de modelos de aprendizado profundo.
    - **`Sequential`**: Estrutura base para a construção do modelo.
    - **`LSTM`**: Camada para redes neurais recorrentes, útil para séries temporais.
    - **`Dense`**: Camada densa totalmente conectada.
    - **`Dropout`**: Técnica de regularização para evitar overfitting.
    - **`EarlyStopping`**: Callback para interromper o treinamento caso o modelo pare de melhorar.

---

## Função Principal: `lstm_stock_prediction`

### **Descrição**
A função treina um modelo LSTM para prever o preço de fechamento de uma ação com base em dados históricos e realiza previsões para um número especificado de dias futuros.

### **Parâmetros**
- `symbol` (str): Símbolo da ação (ex.: 'AAPL', 'MSFT').
- `start_date` (str): Data inicial para obter os dados históricos no formato `'YYYY-MM-DD'`.
- `end_date` (str): Data final para obter os dados históricos no formato `'YYYY-MM-DD'`.
- `future_days` (int): Número de dias futuros para os quais se deseja realizar previsões.

### **Etapas da Função**
1. **Download dos Dados**:
   - Obtém os preços históricos de fechamento usando o `yfinance`.
   - Valida se há dados disponíveis. Caso contrário, retorna um erro.

2. **Normalização**:
   - Os preços de fechamento são normalizados para um intervalo de `[0, 1]` usando `MinMaxScaler`.

3. **Preparação dos Dados**:
   - Cria sequências de dados para entrada (`x_train`) e saída (`y_train`) com base em uma janela deslizante de 60 dias.

4. **Criação do Modelo LSTM**:
   - Estrutura do modelo:
     - 2 camadas LSTM: A primeira com retorno de sequências e a segunda sem.
     - Camadas Dropout para regularização.
     - Camadas Dense para saída intermediária e final.
   - Compilação com otimizador Adam e função de perda `mean_squared_error`.

5. **Treinamento**:
   - O modelo é treinado com `validation_split=0.2` para validação.
   - O treinamento é interrompido automaticamente se a validação não melhorar por 5 épocas consecutivas, utilizando `EarlyStopping`.

6. **Previsão de Dados Futuros**:
   - Utiliza os últimos 60 dias de dados normalizados como entrada.
   - Previsões são geradas iterativamente para o número de dias especificado.

7. **Desnormalização e Formatação**:
   - As previsões são convertidas de volta ao seu valor original utilizando o inverso da escala aplicada.
   - As datas futuras são calculadas e associadas às previsões em um dataframe.

### **Retorno**
- **`predictions_df`** (`pandas.DataFrame`): Contém as datas e os preços de fechamento previstos.

---

### **Exemplo de Uso**
```python
# Importar a função
from lstm_stock_prediction import lstm_stock_prediction

# Prever os preços para a ação AAPL
predicted_prices = lstm_stock_prediction(
    symbol='AAPL',
    start_date='2020-01-01',
    end_date='2023-12-31',
    future_days=30
)

# Visualizar o resultado
print(predicted_prices)

