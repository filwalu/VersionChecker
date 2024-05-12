import os
from cryptography.fernet import Fernet

def decrypt_file(file_path, key):
    cipher_suite = Fernet(key)

    with open(file_path, 'rb') as file:
        encrypted_data = file.read()

    decrypted_data = cipher_suite.decrypt(encrypted_data)

    return decrypted_data.decode()

def read_encrypted_files(directory_path, key):
    decrypted_files = {}

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        decrypted_files[filename] = decrypt_file(file_path, key)

    return decrypted_files

# Wczytywanie klucza
with open("secret.key", "rb") as key_file:
    key = key_file.read()

decrypted_files = read_encrypted_files('fetch/hosts', key)

print(decrypted_files)