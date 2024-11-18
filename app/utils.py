import yfinance as yf  # Biblioteca para obter dados financeiros históricos
import numpy as np  # Biblioteca para cálculos matemáticos e manipulação de arrays
import pandas as pd  # Biblioteca para manipulação de dados tabulares
from sklearn.preprocessing import MinMaxScaler  # Ferramenta para normalizar dados
from keras.models import Sequential  # Para construir modelos de redes neurais
from keras.layers import LSTM, Dense, Dropout  # LSTM para redes recorrentes e Dense para camadas totalmente conectadas
from keras.callbacks import EarlyStopping  # Para aplicar early stopping

def lstm_stock_prediction(symbol, start_date, end_date, future_days):
    # Função para treinar um modelo LSTM e prever o preço de fechamento de uma ação.
    df = yf.download(symbol, start=start_date, end=end_date)
    if df.empty:
        raise ValueError("Nenhum dado foi retornado. Verifique os parâmetros de entrada.")
    
    close_prices = df['Close'].values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(close_prices)

    sequence_length = 60
    x_train, y_train = [], []
    
    for i in range(sequence_length, len(scaled_data)):
        x_train.append(scaled_data[i-sequence_length:i, 0])
        y_train.append(scaled_data[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(25),
        Dense(1)
    ])
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    
    model.fit(x_train, y_train, batch_size=32, epochs=50, verbose=1, validation_split=0.2, callbacks=[early_stopping])

    last_sequence = scaled_data[-sequence_length:]
    predictions = []

    for _ in range(future_days):
        last_sequence = last_sequence.reshape(1, sequence_length, 1)
        predicted_value = model.predict(last_sequence)[0][0]
        predictions.append(predicted_value)
        new_sequence = np.append(last_sequence[0, 1:], [[predicted_value]], axis=0)
        last_sequence = new_sequence

    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

    future_dates = pd.date_range(start=pd.to_datetime(end_date) + pd.Timedelta(days=1), periods=future_days)
    predictions_df = pd.DataFrame({'Date': future_dates, 'Predicted Close': predictions.flatten()})
    
    return predictions_df
