from flask import Blueprint, jsonify
from .utils import lstm_stock_prediction

main_routes = Blueprint('main', __name__)

@main_routes.route('/<symbol>/<start_date>/<end_date>/<int:future_days>', methods=['GET'])
def home(symbol, start_date, end_date, future_days):
    try:
        # Chama a função lstm_stock_prediction com os parâmetros passados na URL
        result = lstm_stock_prediction(symbol, start_date, end_date, future_days)
        # Retorna as previsões em formato JSON
        return jsonify(result.to_dict(orient='records'))  # Converte o DataFrame em um dicionário
    except Exception as e:
        # Retorna erro em formato JSON em caso de falha
        return jsonify({"error": str(e)}), 400
