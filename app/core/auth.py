from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pswrd(password: str) -> str:
    return context.hash(password)

def auth_pass(password: str, pass_hashed: str) -> bool:
    return context.verify(password, pass_hashed)
