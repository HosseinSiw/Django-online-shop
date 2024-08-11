import threading
from mail_templated import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import CustomUser


class EmailThread(threading.Thread):
    def __init__(self, email: EmailMessage):
        threading.Thread.__init__(self)
        self.email = email

    def run(self):
        self.email.send()


def get_token_by_user(user_obj: CustomUser) -> str:
    token = RefreshToken.for_user(user_obj)
    return str(token.access_token)
