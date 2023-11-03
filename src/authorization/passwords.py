import bcrypt


def make_password(password: str) -> str:
    """Creates a password hash."""
    salt = bcrypt.gensalt(rounds=16)
    return bcrypt.hashpw(password.encode(), salt).decode()


def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())
