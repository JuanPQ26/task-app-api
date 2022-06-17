# bcrypt
import bcrypt


def encrypt_password(password: str) -> str:
    password_hashed = bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt())
    password_hashed_str = str(password_hashed, "UTF-8")

    return password_hashed_str


def validate_password(password: str, hashed: str) -> bool:
    password = bytes(password, 'utf-8')
    hashed = bytes(hashed, 'utf-8')

    if bcrypt.checkpw(password, hashed):
        return True
    else:
        return False
