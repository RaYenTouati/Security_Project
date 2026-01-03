# cryptanalysis_tool/ciphers/affine.py

import math
from ..analysis.scoring import calculate_score

def modular_inverse(a, m):
    """
    Calcule l'inverse modulaire de a modulo m via l'algorithme d'Euclide étendu.
    Ou utilise pow(a, -1, m) si disponible (Python 3.8+).
    Retourne None si l'inverse n'existe pas.
    """
    try:
        return pow(a, -1, m)
    except ValueError:
        return None

def decrypt(text, a, b):
    """
    Déchiffre un texte chiffré par Affine avec les clés a et b.
    Fonction de déchiffrement : D(y) = a^-1 * (y - b) mod 26
    """
    m = 26
    a_inv = modular_inverse(a, m)
    
    if a_inv is None:
        return None  # Clé 'a' invalide
        
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            y = ord(char) - base
            # Déchiffrement
            x = (a_inv * (y - b)) % m
            result.append(chr(base + x))
        else:
            result.append(char)
    return "".join(result)

def break_cipher(ciphertext):
    """
    Teste toutes les combinaisons valides de a et b.
    a doit être premier avec 26.
    b entre 0 et 25.
    """
    candidates = []
    # Valeurs possibles pour a (copremiers avec 26)
    valid_a = [i for i in range(1, 26) if math.gcd(i, 26) == 1]
    
    for a in valid_a:
        for b in range(26):
            plaintext = decrypt(ciphertext, a, b)
            if plaintext:
                metrics = calculate_score(plaintext)
                candidates.append({
                    "cipher": "Affine",
                    "key": {"a": a, "b": b},
                    "plaintext": plaintext,
                    "metrics": metrics
                })
                
    # Tri des candidats
    # calculate_score retourne un score global 'score' (plus c'est haut mieux c'est)
    candidates.sort(key=lambda x: x['metrics']['score'], reverse=True)
    
    return candidates
