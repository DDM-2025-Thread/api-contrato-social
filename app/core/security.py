from passlib.context import CryptContext
import secrets
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def generate_api_key(length: int = 32) -> str:
    return secrets.token_hex(length)

def hash_api_key(api_key: str):
    key_bytes = api_key.encode('utf-8')
    
    hashed_bytes = hashlib.sha256(key_bytes).digest()
    
    hashed_key_hex = hashed_bytes.hex()
    return hashed_key_hex

def verify_api_key_hash(plain_api_key: str, hashed_api_key: str):
    incoming_hash = hash_api_key(plain_api_key)
    return secrets.compare_digest(incoming_hash, hashed_api_key)
