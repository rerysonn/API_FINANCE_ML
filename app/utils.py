import yfinance as yf  # Biblioteca para obter dados financeiros históricos
import numpy as np  # Biblioteca para cálculos matemáticos e manipulação de arrays
import pandas as pd  # Biblioteca para manipulação de dados tabulares
from sklearn.preprocessing import MinMaxScaler  # Ferramenta para normalizar dados
from keras.models import Sequential  # Para construir modelos de redes neurais
from keras.layers import LSTM, Dense, Dropout  # LSTM para redes recorrentes e Dense para camadas totalmente conectadas
from keras.callbacks import EarlyStopping  # Para aplicar early stopping

def lstm_stock_prediction(symbol, start_date, end_date, future_days):
    # Baixa os dados históricos de preços de ações usando a biblioteca yfinance.
    # O `symbol` é o código da ação, `start_date` e `end_date` são os limites do intervalo de tempo.
    df = yf.download(symbol, start=start_date, end=end_date)
    
    # Verifica se os dados retornados estão vazios. Se sim, levanta uma exceção.
    if df.empty:
        raise ValueError("Nenhum dado foi retornado. Verifique os parâmetros de entrada.")
    
    # Extrai os preços de fechamento da ação e redimensiona para um formato de matriz 2D.
    close_prices = df['Close'].values.reshape(-1, 1)
    
    # Normaliza os preços de fechamento para o intervalo [0, 1], o que ajuda na convergência do modelo.
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(close_prices)

    # Define o comprimento das sequências de entrada (60 dias de dados históricos).
    sequence_length = 60
    
    # Inicializa listas para armazenar os dados de entrada (x_train) e os valores esperados de saída (y_train).
    x_train, y_train = [], []
    
    # Cria as sequências de dados para treinar o modelo.
    for i in range(sequence_length, len(scaled_data)):
        # Adiciona uma sequência de 60 preços consecutivos como entrada.
        x_train.append(scaled_data[i-sequence_length:i, 0])
        # Adiciona o preço seguinte como saída.
        y_train.append(scaled_data[i, 0])

    # Converte as listas para arrays NumPy.
    x_train, y_train = np.array(x_train), np.array(y_train)
    
    # Redimensiona x_train para incluir uma dimensão adicional (necessária para LSTMs).
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # Define o modelo de rede neural LSTM.
    model = Sequential([
        # Primeira camada LSTM com 50 neurônios e retorno de sequências ativado.
        LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)),
        # Adiciona Dropout para evitar overfitting.
        Dropout(0.2),
        # Segunda camada LSTM com 50 neurônios, sem retorno de sequências.
        LSTM(50, return_sequences=False),
        # Outro Dropout.
        Dropout(0.2),
        # Camada densa com 25 neurônios.
        Dense(25),
        # Camada de saída com 1 neurônio (previsão do preço de fechamento).
        Dense(1)
    ])
    
    # Compila o modelo usando o otimizador Adam e a função de perda de erro quadrático médio.
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    # Configura o EarlyStopping para interromper o treinamento quando o desempenho no conjunto de validação não melhorar.
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    
    # Treina o modelo nos dados de treinamento.
    model.fit(x_train, y_train, batch_size=32, epochs=50, verbose=1, validation_split=0.2, callbacks=[early_stopping])

    # Prepara a última sequência de dados para começar as previsões futuras.
    last_sequence = scaled_data[-sequence_length:]
    predictions = []

    # Gera previsões para o número de dias futuros especificado.
    for _ in range(future_days):
        # Redimensiona a sequência para o formato necessário pelo modelo.
        last_sequence = last_sequence.reshape(1, sequence_length, 1)
        # Faz uma previsão para o próximo dia.
        predicted_value = model.predict(last_sequence)[0][0]
        # Adiciona a previsão à lista de previsões.
        predictions.append(predicted_value)
        # Atualiza a sequência com o valor previsto.
        new_sequence = np.append(last_sequence[0, 1:], [[predicted_value]], axis=0)
        last_sequence = new_sequence

    # Desnormaliza os valores previstos para retornar aos preços originais.
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

    # Cria datas futuras correspondentes às previsões.
    future_dates = pd.date_range(start=pd.to_datetime(end_date) + pd.Timedelta(days=1), periods=future_days)
    
    # Cria um DataFrame com as datas futuras e os preços previstos.
    predictions_df = pd.DataFrame({'Date': future_dates, 'Predicted Close': predictions.flatten()})
    
    # Retorna o DataFrame contendo as previsões.
    return predictions_df
