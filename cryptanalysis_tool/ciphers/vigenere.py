# cryptanalysis_tool/ciphers/vigenere.py

def encrypt(plaintext: str, key: str) -> str:
    """
    Chiffre un texte avec le chiffre de Vigenère.
    
    Args:
        plaintext (str): Le texte à chiffrer.
        key (str): La clé de chiffrement (lettres).
        
    Returns:
        str: Le texte chiffré.
    """
    if not key:
        return plaintext
        
    key_indices = [ord(k.upper()) - ord('A') for k in key if k.isalpha()]
    if not key_indices:
        return plaintext
        
    result = []
    key_idx = 0
    key_len = len(key_indices)
    
    for char in plaintext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = key_indices[key_idx % key_len]
            
            encoded = (ord(char) - base + shift) % 26
            result.append(chr(base + encoded))
            
            key_idx += 1
        else:
            result.append(char)
            
    return "".join(result)

def decrypt(ciphertext: str, key: str) -> str:
    """
    Déchiffre un texte chiffré par Vigenère.
    
    Args:
        ciphertext (str): Le texte chiffré.
        key (str): La clé de chiffrement.
        
    Returns:
        str: Le texte déchiffré.
    """
    if not key:
        return ciphertext

    # Pour déchiffrer Vigenère, on peut utiliser encrypt avec la clé inverse ?
    # Non, pour Vigenère chiffrer c'est (c + k), déchiffrer c'est (c - k).
    # On peut précalculer la clé de déchiffrement ou le faire au vol.
    
    key_indices = [ord(k.upper()) - ord('A') for k in key if k.isalpha()]
    if not key_indices:
        return ciphertext
        
    result = []
    key_idx = 0
    key_len = len(key_indices)
    
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = key_indices[key_idx % key_len]
            
            # Déchiffrement : (char - shift)
            decoded = (ord(char) - base - shift) % 26
            result.append(chr(base + decoded))
            
            key_idx += 1
        else:
            result.append(char)
            
    return "".join(result)
