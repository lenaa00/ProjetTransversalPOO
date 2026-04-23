import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

# Pour générer les clés publiques er privées
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()

# Pour sauvegarder la clé privée
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

# Pour sauvegarder  la clé publique
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Pour lire les clés
loaded_private_key = serialization.load_pem_private_key(private_pem, password=None)
loaded_public_key = serialization.load_pem_public_key(public_pem)


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

# Test cryptage et décryptage
#data = b"Voici un message secret"
#encrypted_data = encrypt(data, public_key)
#print("Données chiffrées :", encrypted_data)
#decrypted_data = decrypt(encrypted_data, private_key)
#print("Données déchiffrées :", decrypted_data.decode())


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


# Pour tester le salage
data = "Voici les données à hacher".encode("utf-8")
salt, salted_data = add_salt(data)
hashed_data = hash_data(salted_data)
print("Salt:", salt)
print("Hash:", hashed_data)

# Pour hasher un mot de passe avec un sel
def hash_password_with_salt(password: str) -> tuple[str, str]:
    data = password.encode("utf-8")
    salt = os.urandom(16)
    salted = salt + data
    hashed = hash_data(salted)
    return salt.hex(), hashed.hex()

# Test hashage de mot de passe
def verify_password(password: str, salt_hex: str, stored_hash_hex: str) -> bool:
    salt = bytes.fromhex(salt_hex)
    data = password.encode("utf-8")
    salted = salt + data
    hashed = hash_data(salted).hex()
    return hashed == stored_hash_hex