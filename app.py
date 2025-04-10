from flask import Flask, request, redirect, make_response
import requests
from uuid import uuid4
import sys
import io

# Исправление кодировки для Windows-консоли
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Временное хранилище для токенов
temp_storage = {}

@app.route('/')
def home():
    return redirect('/auth')

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        client_id = request.form.get('client_id')
        secret_key = request.form.get('secret_key')

        if not client_id or not secret_key:
            return "Укажите ID приложения и секретный ключ", 400

        session_id = str(uuid4())

        temp_storage[session_id] = {
            'client_id': client_id,
            'secret_key': secret_key
        }

        redirect_uri = 'http://localhost/api/v1/auth/vk/callback'
        scopes = 'notify,friends,photos,audio,video,docs,notes,pages,status,offers,questions,wall,groups,messages,email,notifications,stats,ads,market,offline'
        auth_url = f"https://oauth.vk.com/authorize?client_id={client_id}&display=page&redirect_uri={redirect_uri}&scope={scopes}&response_type=code&v=5.131&state={session_id}"

        response = make_response(redirect(auth_url))
        response.set_cookie('vk_session_id', session_id)
        return response

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Авторизация VK</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }
            input, button { width: 100%; padding: 10px; margin: 8px 0; box-sizing: border-box; }
        </style>
    </head>
    <body>
        <h2>Получить токен доступа ВКонтакте</h2>
        <form method="POST">
            <label>ID приложения:</label>
            <input type="text" name="client_id" required>

            <label>Секретный ключ:</label>
            <input type="text" name="secret_key" required>

            <button type="submit">Получить токен</button>
        </form>

        <div id="tokenBlock" style="display: none;">
            <h3>Ваш токен:</h3>
            <input type="text" id="tokenField" readonly>
            <button onclick="copyToken()">Скопировать</button>
        </div>

        <script>
            function copyToken() {
                const input = document.getElementById('tokenField');
                input.select();
                input.setSelectionRange(0, 99999); // для мобильных
                document.execCommand('copy');
        
                // Показываем всплывающее окно
                const alertMessage = document.createElement('div');
                alertMessage.textContent = 'Токен скопирован!';
                alertMessage.style.position = 'fixed';
                alertMessage.style.top = '20px';
                alertMessage.style.left = '50%';
                alertMessage.style.transform = 'translateX(-50%)';
                alertMessage.style.padding = '10px 20px';
                alertMessage.style.backgroundColor = '#4CAF50';
                alertMessage.style.color = 'white';
                alertMessage.style.borderRadius = '5px';
                document.body.appendChild(alertMessage);
        
                // Скрываем блок с токеном и кнопкой
                document.getElementById('tokenBlock').style.display = 'none';
        
                // Убираем всплывающее окно через 3 секунды
                setTimeout(() => {
                    alertMessage.style.display = 'none';
                }, 3000);
            }
        
            const urlParams = new URLSearchParams(window.location.search);
            const token = urlParams.get('access_token');
            if (token) {
                document.getElementById('tokenField').value = token;
                document.getElementById('tokenBlock').style.display = 'block';
            }
        </script>

    </body>
    </html>
    """

@app.route('/api/v1/auth/vk/callback')
def callback():
    code = request.args.get('code')
    session_id = request.args.get('state') or request.cookies.get('vk_session_id')

    if not code or not session_id:
        return "Ошибка авторизации", 400

    client_data = temp_storage.pop(session_id, None)
    if not client_data:
        return "Сессия устарела", 400

    params = {
        'client_id': client_data['client_id'],
        'client_secret': client_data['secret_key'],
        'redirect_uri': 'http://localhost/api/v1/auth/vk/callback',
        'code': code
    }

    response = requests.get("https://oauth.vk.com/access_token", params=params)
    if response.status_code != 200:
        return f"Ошибка VK: {response.text}", 400

    token_data = response.json()
    if 'error' in token_data:
        return f"Ошибка VK: {token_data.get('error_description', 'Неизвестная ошибка')}", 400

    # Возвращаем токен на страницу
    return redirect(f"/auth?access_token={token_data['access_token']}")

@app.after_request
def add_charset(response):
    if "text/html" in response.content_type:
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

def run_server():
    try:
        app.run(host='0.0.0.0', port=80)
    except OSError:
        print("\n❌ Ошибка: Порт 80 занят.")
        print("Попробуйте закрыть другие процессы, использующие порт 80.")
        exit(1)

if __name__ == '__main__':
    run_server()
