from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__)

# Serve o arquivo index.html
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/webhook/joke', methods=['POST'])
def webhook_joke():
    data = request.get_json()
    lang = data.get('lang', 'en')
    blacklist = data.get('blacklist', [])

    valid_languages = ['en', 'cs', 'de', 'es', 'fr', 'pt']
    if lang not in valid_languages:
        error_message = f'Idioma inválido. Idiomas suportados: {", ".join(valid_languages)}'
        return jsonify({'error': error_message}), 400

    try:
        joke_url = f'https://v2.jokeapi.dev/joke/Any?lang={lang}&blacklistFlags={",".join(blacklist)}'
        response = requests.get(joke_url)
        response.raise_for_status()
        
        joke_data = response.json()
        joke = joke_data.get('joke') or f"{joke_data.get('setup')} ... {joke_data.get('delivery')}"

        return jsonify({'joke': joke}), 200
    
    except requests.RequestException as e:
        print(f'Erro ao buscar piada da JokeAPI: {e}')
        return jsonify({'error': 'Erro ao buscar piada da JokeAPI'}), 500

if __name__ == '__main__':
    app.run(port=5000)
