import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

SEL_UNIQUE = "MichaelJackson"

# Pour générer les clés publiques et privées
def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem, public_pem



# Pour chiffrer les données en utilisant la clé publique
def encrypt(data, public_key):
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

# Pour déchiffrer les données chiffrées en utilisant la clé privée
def decrypt(encrypted_data, private_key):
    return private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


# Pour hasher les données
def hash_data(data):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(data)
    return digest.finalize()


# Test hashage
#data = "Voici les données à hacher"
#hashed_data = hash_data(data.encode("utf-8"))
#print("Données hachées :", hashed_data.hex())

# Pour saler les données 
def add_salt(data):
    salt = os.urandom(16)
    return salt, salt + data


# Pour hasher un mot de passe avec un sel
def hash_password_with_salt(password: str) -> tuple[str, str]:
    data = password.encode("utf-8")
    salt = os.urandom(16)
    salted = salt + data
    hashed = hash_data(salted)
    return salt.hex(), hashed.hex()


def verify_password(password: str, salt_hex: str, stored_hash_hex: str) -> bool:
    salt = bytes.fromhex(salt_hex)
    data = password.encode("utf-8")
    salted = salt + data
    hashed = hash_data(salted).hex()
    return hashed == stored_hash_hex

