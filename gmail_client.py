import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailClient:
    def __init__(self, credentials_path='credentials.json', token_path='token.json'):
        self.creds = None
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = self._authenticate()

    def _authenticate(self):
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(self.token_path, 'w') as f:
                f.write(creds.to_json())
        self.creds = creds
        return build('gmail', 'v1', credentials=creds)

    def list_messages(self, query='newer_than:7d', max_results=10):
        res = self.service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
        return res.get('messages', []) or []

    def get_message(self, msg_id):
        msg = self.service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        return msg

    def download_attachment(self, msg_id, attachment_id, filename):
        att = self.service.users().messages().attachments().get(userId='me', messageId=msg_id, id=attachment_id).execute()
        data = att.get('data')
        file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as f:
            f.write(file_data)
        return filename
