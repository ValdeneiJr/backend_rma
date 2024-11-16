from pwdlib import PasswordHash

hashing = PasswordHash.recommended()

def hashing_senha(senha):
    return hashing.hash(senha)

def verificar_senha(senha, hash_senha):
    return hashing.verify(senha, hash_senha)
