from pathlib import Path
import pickle
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# variaveis do .env
load_dotenv()

SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
]

# ler o .env
TOKEN_FILE = Path('token.pickle')
CREDENTIALS_FILE = Path('credentials/client_secret.json')

def get_credentials():
        """
        Pega as credenciais de autenticação.
        """

        creds = None

        # Verifica se já existe um token salvo
        if TOKEN_FILE.exists():
            print("Carregando token salvo...")
            try:
                with open(TOKEN_FILE, 'rb') as token:
                    creds = pickle.load(token)
            except Exception as e:
                print(f"Token corrompido ou inválido: {e}")
                print("   Fazendo novo login...")
                TOKEN_FILE.unlink()  # Apaga o arquivo ruim
                creds = None

        # Se não tem credencial, ou se expirou, renovar ou pedir novo login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("Renovando token expirado...")
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Erro ao renovar: {e}")
                    print("   Fazendo novo login...")
                    creds = None

            if not creds:  # Se ainda não tem credencial, faz novo login
                print("Abrindo navegador para você autenticar...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CREDENTIALS_FILE), SCOPES)
                creds = flow.run_local_server(port=0)

            # Salva o token pra próxima vez
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
                print("✓ Token salvo com sucesso")

        return creds


def get_service():
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds, static_discovery=False)

    return service

if __name__ == '__main__':
    print("Testando autenticação...")
    service = get_service()

    profile = service.users().getProfile(userId='me').execute()
    print(f"Autenticado como: {profile['emailAddress']}")
    print(f"Mensagem na caixa de entrada: {profile['messagesTotal']}")












