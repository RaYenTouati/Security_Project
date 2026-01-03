# verification_test.py

import sys
# Ajout du dossier courant au path pour les imports
sys.path.append('.')

from cryptanalysis_tool.ciphers import caesar, affine
from cryptanalysis_tool.ciphers.bruteforce import get_caesar_candidates
from cryptanalysis_tool.analysis.scoring import calculate_score

def test_caesar():
    print("[-] Testing Caesar Cipher...")
    # "CECI EST UN TEST SECRET" (shift 1) -> "DFDJ FTU VO UFTU TFDSFU"
    ciphertext = "DFDJ FTU VO UFTU TFDSFU"
    expected = "CECI EST UN TEST SECRET"
    
    # New API: get candidates, then score
    candidates = get_caesar_candidates(ciphertext)
    for c in candidates:
        metrics = calculate_score(c['plaintext'])
        c['score'] = metrics['score']
        
    candidates.sort(key=lambda x: x['score'], reverse=True)
    best = candidates[0]
    
    print(f"    Input: {ciphertext}")
    print(f"    Best guess: {best['plaintext']} (Key: {best['key']})")
    
    # Note: bruteforce.py returns key as int, old was dict {'shift': shift} maybe? 
    # Let's check logic: if best key is 1, it passes.
    if best['plaintext'] == expected and best['key'] == 1:
        print("    [PASS] Caesar check")
        return True
    else:
        print(f"    [FAIL] Expected {expected}, got {best['plaintext']}")
        return False

def test_affine():
    print("[-] Testing Affine Cipher...")
    # "LA SECURITE EST IMPORTANTE"
    # a=5, b=8
    # L -> (5*11 + 8) % 26 = 63 % 26 = 11 -> L (Self mapping for L? 55+8=63. 63/26=2r11. Yes L->L)
    # A-> (5*0+8) = H
    # ... let's trust a generator.
    # a=5, b=8. inverse a=21.
    # L(11) -> L(11). A(0) -> I(8).
    # "LIA S..." wait, let's use a simpler known pair manually or trust the tool.
    # Let's use the code to ENCRYPT first to be sure.
    
    plaintext = "LA SECURITE EST IMPORTANTE" # 24 chars
    a, b = 5, 8
    
    # Encrypt manually logic
    encrypted = ""
    for char in plaintext:
        if char.isalpha():
            base = ord('A')
            x = ord(char) - base
            y = (a * x + b) % 26
            encrypted += chr(base + y)
        else:
            encrypted += char
            
    print(f"    Generated Ciphertext: {encrypted}")
    
    candidates = affine.break_cipher(encrypted)
    best = candidates[0]
    
    print(f"    Best guess: {best['plaintext']} (Key: {best['key']})")
    
    if best['plaintext'] == plaintext and best['key']['a'] == a and best['key']['b'] == b:
        print("    [PASS] Affine check")
        return True
    else:
        print(f"    [FAIL] Expected {plaintext}, got {best['plaintext']}")
        return False

if __name__ == "__main__":
    if test_caesar() and test_affine():
        print("\n[SUCCESS] All tests passed!")
        sys.exit(0)
    else:
        print("\n[FAILURE] Some tests failed.")
        sys.exit(1)
