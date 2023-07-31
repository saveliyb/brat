import secrets
import hashlib


def hash_password(password: str, salt: str):
    h = hashlib.blake2b(salt=salt)
    h.update(password.encode())
    return h.hexdigest()


def generate_salt():
    return secrets.token_bytes(16)


def hash_victim_id(_id: int):
    h = hashlib.blake2b()
    h.update(str(_id).encode())
    return h.hexdigest()