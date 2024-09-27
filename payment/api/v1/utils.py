import threading
from mail_templated import EmailMessage


class OrderEmailThread(threading.Thread):
    """
    This is a multi thread Email sender for using after an order is saved.
    """
    def __init__(self, email: EmailMessage):
        threading.Thread.__init__(self)
        self.email = email

    def run(self):
        self.email.send()
