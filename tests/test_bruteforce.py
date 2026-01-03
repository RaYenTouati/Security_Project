# tests/test_bruteforce.py
import pytest
from cryptanalysis_tool.ciphers.caesar import encrypt
from cryptanalysis_tool.ciphers.bruteforce import get_caesar_candidates

def test_bruteforce_candidates_count():
    # On chiffre un texte
    plaintext = "Ceci est un test de bruteforce."
    shift = 10
    ciphertext = encrypt(plaintext, shift)
    
    candidates = get_caesar_candidates(ciphertext)
    
    # Doit retourner 25 candidats
    assert len(candidates) == 25
    
    # L'un des candidats doit être le bon (shift 10 => key correspondante)
    # Note: si on déchiffre avec shift 10, la clé est encrypt shift.
    # Dans get_caesar_candidates, k est la clé de **déchiffrement**.
    # encrypt(p, 10) => decrypt(c, 10) recovers p.
    # Donc candidate avec key=10 doit être plaintext.
    
    found = False
    for c in candidates:
        if c['key'] == 10:
            if c['plaintext'] == plaintext:
                found = True
                break
    assert found
