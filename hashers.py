from django.contrib.auth.hashers import PBKDF2PasswordHasher
from hashlib import sha512


class CustomPBKDF2PasswordHasher(PBKDF2PasswordHasher):
    iterations = 5_000_000
    algorithm = 'pbkdf2_sha512_custom'
    digest = sha512
