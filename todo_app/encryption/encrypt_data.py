"""
This file contains code to encrypt and decrypt data
"""
from cryptography.fernet import Fernet


def generate_key():
    """
    :return: generate and return key
    """
    return Fernet.generate_key()


def encrypt_data(key, data):
    """
    encrypt data
    :param key: str
    :param data: json
    :return: byte string
    """
    cipher_suite = Fernet(key)
    data_bytes = str(data).encode()
    encrypted_data = cipher_suite.encrypt(data_bytes)
    return encrypted_data


def decrypt_data(key, encrypted_data):
    """
        decrypt data
        :param key: str
        :param encrypted_data: byte str
        :return: str of json
        """
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    return decrypted_data.decode()
