import os
import base64
import getpass
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend

def get_password():
    return getpass.getpass("🔑 Enter a password for this file: ").encode()

def derive_fernet_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password))

def save_file_key(file_stem, aes_key):
    password = get_password()
    salt = os.urandom(16)
    
    # Save the salt to a file
    with open(f"{file_stem}.salt", "wb") as f:
        f.write(salt)

    # Derive Fernet key from the password and salt
    fernet_key = derive_fernet_key(password, salt)
    fernet = Fernet(fernet_key)

    # Encrypt the AES key with the Fernet key
    encrypted_aes = fernet.encrypt(aes_key)

    # Save the encrypted AES key to a file
    with open(f"{file_stem}.key", "wb") as f:
        f.write(encrypted_aes)

def load_file_key(file_stem):
    # Ensure that both the key and salt files exist
    if not os.path.exists(f"{file_stem}.key") or not os.path.exists(f"{file_stem}.salt"):
        print("❌ Key or salt file missing.")
        return None

    # Get the password from the user
    password = get_password()

    # Read the salt from the file
    with open(f"{file_stem}.salt", "rb") as f:
        salt = f.read()

    # Derive the Fernet key from the password and salt
    fernet_key = derive_fernet_key(password, salt)
    fernet = Fernet(fernet_key)

    # Read the encrypted AES key from the file
    with open(f"{file_stem}.key", "rb") as f:
        encrypted_key = f.read()

    try:
        # Decrypt the AES key using the Fernet key
        return fernet.decrypt(encrypted_key)
    except Exception as e:
        print("❌ Wrong password or corrupted key.")
        return None
