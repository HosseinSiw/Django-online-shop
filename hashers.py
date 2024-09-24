from django.contrib.auth.hashers import PBKDF2PasswordHasher


class CustomPasswordHasher(PBKDF2PasswordHasher):
    iterations = 5_000_000_000
    algorithm = 'pbkdf2_sha256_custom'
    digest = 'sha512'
