# cryptanalysis_tool/main.py

import sys
import argparse
from cryptanalysis_tool.ciphers import caesar, affine

def print_banner():
    print("=======================================================")
    print("   OUITL DE CRYPTANALYSE AUTOMATIQUE - PROJET PERSO    ")
    print("=======================================================")
    print("Philosophie: 'Comprendre pour mieux protéger'")
    print("-------------------------------------------------------")

def analyze_ciphertext(text):
    print(f"\n[*] Analyse du message : {text[:50]}...")
    print(f"[*] Longueur : {len(text)} caractères")
    
    results = []
    
    # 1. Test César
    print("[*] Test des hypothèses César...")
    caesar_candidates = caesar.break_cipher(text)
    if caesar_candidates:
        results.extend(caesar_candidates)
        
    # 2. Test Affine
    print("[*] Test des hypothèses Affine...")
    affine_candidates = affine.break_cipher(text)
    if affine_candidates:
        results.extend(affine_candidates)
        
    # Tri global des résultats
    # Priorité : % de mots reconnus, puis score chi-carré
    results.sort(key=lambda x: (-x['metrics']['word_match_percent'], x['metrics']['chi_squared']))
    
    return results

def format_result(candidate, rank):
    metrics = candidate['metrics']
    key_str = ", ".join(f"{k}={v}" for k, v in candidate['key'].items())
    
    return (
        f"--- Candidat #{rank} ---\n"
        f"Chiffrement : {candidate['cipher']}\n"
        f"Clé         : {key_str}\n"
        f"Score Mots  : {metrics['word_match_percent']:.1f}%\n"
        f"Chi-Carré   : {metrics['chi_squared']:.2f}\n"
        f"Message     : {candidate['plaintext'][:100]}...\n"
    )

def main():
    print_banner()
    
    if len(sys.argv) > 1:
        ciphertext = " ".join(sys.argv[1:])
    else:
        # Message par défaut ou invite
        print("\nEntrez le message chiffré à analyser (ou appuyez sur Entrée pour un test par défaut):")
        try:
            user_input = input("> ").strip()
            if not user_input:
                # Phrase test : "LE DECRYPTAGE EST UN SUCCES" (César +3) -> "OH GHFUBSWDJH HVW XQ VXFFHV"
                ciphertext = "OH GHFUBSWDJH HVW XQ VXFFHV"
                print(f"\n[!] Aucun message entré. Utilisation du message de test : {ciphertext}")
            else:
                ciphertext = user_input
        except EOFError:
             return

    top_candidates = analyze_ciphertext(ciphertext)
    
    print("\n=== RÉSULTATS DE L'ANALYSE ===\n")
    
    # Afficher les 3 meilleurs candidats
    for i, candidate in enumerate(top_candidates[:3], 1):
        print(format_result(candidate, i))
        
    best = top_candidates[0]
    print("\n=== DÉCISION DE L'ANALYSTE ===")
    
    if best['metrics']['word_match_percent'] > 40:
        print(f"L'analyse est CONFIANTE.\n"
              f"Le message semble être chiffré avec {best['cipher']} (Clé: {best['key']}).\n"
              f"Une proportion significative de mots français a été détectée.")
    else:
        print("L'analyse est INCERTAINE.\n"
              "Les scores de reconnaissance de mots sont faibles.\n"
              "Le message est peut-être chiffré avec une autre méthode, "
              "ou le texte est trop court ou dans une autre langue.")

if __name__ == "__main__":
    main()
