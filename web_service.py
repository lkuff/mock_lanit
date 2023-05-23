from flask import Flask, request, jsonify

app = Flask(__name__)

# Обработка POST-запроса по пути "/json"
@app.route('/json', methods=['POST'])
def update_user_info():
    # Получение параметра action из URL-запроса
    action = request.args.get('action')

    # Проверка параметра action и выполнение соответствующих действий
    if action == 'add':
        # Получение данных из JSON-запроса
        data = request.get_json()
        ticker_name = data['add']['name']
        time_frame = data['add']['timeFrame']
        percent = data['add']['percent']

        # Добавление оповещения в список тикеров JSON
        tickers = data['info']['tickers']
        ticker_found = False
        for ticker in tickers:
            if ticker['ticker'] == ticker_name:
                ticker['alerts'].append({
                    'timeframe': time_frame,
                    'percent': percent
                })
                ticker_found = True
                break

        # Если тикер не найден, добавляем новый тикер
        if not ticker_found:
            tickers.append({
                'ticker': ticker_name,
                'alerts': [{
                    'timeframe': time_frame,
                    'percent': percent
                }]
            })

        # Построение и возврат JSON-ответа
        response = {
            'info': data['info'],
            'uuid': data['uuid'],
            'lastUpdate': data['lastUpdate']
        }
        return jsonify(response)

    elif action == 'delete':
        # Получение данных из JSON-запроса
        data = request.get_json()
        ticker_name = data['delete']['tickerName']
        alert_index = data['delete']['alertIndex']

        # Удаление оповещения из списка тикеров JSON
        tickers = data['info']['tickers']
        ticker_found = False
        for ticker in tickers:
            if ticker['ticker'] == ticker_name:
                alerts = ticker['alerts']
                if alert_index < len(alerts):
                    del alerts[alert_index]
                    ticker_found = True
                break

        # Если тикер не найден, возвращаем ошибку 404
        if not ticker_found:
            return jsonify({'error': 'Передан некорректный тикер'}), 404

        # Построение и возврат JSON-ответа
        response = {
            'info': data['info'],
            'uuid': data['uuid'],
            'lastUpdate': data['lastUpdate']
        }
        return jsonify(response)

    else:
        # Возвращаем ошибку 400 при некорректном значении параметра action
        return jsonify({'error': f'Передан некорректный action - {action}'}), 400

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
