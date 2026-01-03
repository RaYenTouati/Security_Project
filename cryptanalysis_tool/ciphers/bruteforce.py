# cryptanalysis_tool/ciphers/bruteforce.py

from .caesar import decrypt

def get_caesar_candidates(ciphertext: str):
    """
    Génère les 25 candidats de déchiffrement César (clés 1..25).
    
    Args:
        ciphertext (str): Le texte chiffré.
        
    Returns:
        list[dict]: Une liste de dictionnaires contenant la clé, le texte clair et un extrait.
    """
    candidates = []
    
    # On teste les décalages de 1 à 25
    for k in range(1, 26):
        plaintext = decrypt(ciphertext, k)
        excerpt = plaintext[:120] if len(plaintext) > 120 else plaintext
        
        candidate = {
            "key": k,
            "plaintext": plaintext,
            "excerpt": excerpt
        }
        candidates.append(candidate)
        
    return candidates
