# cryptanalysis_tool/ciphers/caesar.py

def encrypt(plaintext: str, shift: int) -> str:
    """
    Chiffre un texte avec le chiffre de César.
    
    Args:
        plaintext (str): Le texte à chiffrer.
        shift (int): Le décalage (clé).
        
    Returns:
        str: Le texte chiffré.
        
    Preserves case, punctuation, and non-alphabetic characters.
    """
    result = []
    for char in plaintext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            # (char + shift)
            encoded = (ord(char) - base + shift) % 26
            result.append(chr(base + encoded))
        else:
            result.append(char)
    return "".join(result)

def decrypt(ciphertext: str, shift: int) -> str:
    """
    Déchiffre un texte chiffré par César avec un décalage donné.
    
    Args:
        ciphertext (str): Le texte chiffré.
        shift (int): Le décalage (clé).
        
    Returns:
        str: Le texte déchiffré.
        
    Preserves case, punctuation, and non-alphabetic characters.
    """
    return encrypt(ciphertext, -shift)
