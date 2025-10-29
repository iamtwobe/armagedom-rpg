from src.utils.config import Config
import requests
import secrets



def send_dm_to_user(user_id: int, message: str):
    code = secrets.token_hex(12)
    full_message = f"{message} {code}"
    
    payload = {
        'user_id': user_id,
        'message': full_message
    }
    
    headers = {
        'Authorization': Config.BOT_SECRET,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(
            Config.BOT_WEBHOOK_URL, 
            json=payload, 
            headers=headers, 
            timeout=5
        )
        
        if response.status_code == 200 and response.text == 'ok':
            return code
        elif response.status_code == 403:
            return 'error Usuário não está no servidor'
        elif response.status_code == 404:
            return 'error Usuário não encontrado'
        elif response.status_code == 401:
            return 'error Erro de autenticação interna'
        else:
            return f'error Falha do Bot: {response.text}'

    except requests.exceptions.Timeout:
        return 'error Bot Webhook não respondeu (Timeout)'
    except requests.exceptions.ConnectionError:
        return 'error O Bot Webhook está offline ou não está rodando na porta correta.'
    except Exception as e:
        return f'error Falha inesperada: {e}'