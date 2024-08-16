from rest_framework_simplejwt.tokens import RefreshToken
from ..models import CustomUser
import threading
from mail_templated import EmailMessage


def get_token_for_user(user: CustomUser) -> str:
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


class EmailThread(threading.Thread):
    def __init__(self, email: EmailMessage):
        threading.Thread.__init__(self)
        self.email = email

    def run(self):
        self.email.send()
