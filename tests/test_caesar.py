# tests/test_caesar.py
import pytest
from cryptanalysis_tool.ciphers.caesar import encrypt, decrypt

def test_caesar_invertibility():
    plaintext = "Hello World!"
    shift = 7
    ciphertext = encrypt(plaintext, shift)
    decrypted = decrypt(ciphertext, shift)
    assert decrypted == plaintext

def test_caesar_punctuation():
    text = "Hello, World!"
    encrypted = encrypt(text, 1)
    assert "," in encrypted
    assert " " in encrypted
    # 'H' -> 'I', 'W' -> 'X'
    assert encrypted == "Ifmmp, Xpsme!"

def test_empty():
    assert encrypt("", 5) == ""
    assert decrypt("", 5) == ""
