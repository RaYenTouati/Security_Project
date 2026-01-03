# bin/crack.py
import sys
import os
import argparse
import json
import logging

# Ajout du chemin racine pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cryptanalysis_tool.ciphers.bruteforce import get_caesar_candidates
from cryptanalysis_tool.analysis.vigenere_crack import crack_vigenere
from cryptanalysis_tool.analysis.scoring import calculate_score, detect_language

def main():
    parser = argparse.ArgumentParser(description="Outil de Cryptanalyse (César + Vigenère)")
    parser.add_argument("--input", "-i", type=str, required=True, help="Texte chiffré à analyser")
    parser.add_argument("--top", "-n", type=int, default=5, help="Nombre de meilleures solutions à afficher")
    parser.add_argument("--lang", "-l", type=str, choices=['fr', 'en'], help="Langue supposée (auto-détection si absent)")
    parser.add_argument("--json", action="store_true", help="Sortie JSON stricte")
    parser.add_argument("--model", type=str, help="Chemin vers le modèle ML (optionnel)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Logs verbeux")
    
    args = parser.parse_args()
    
    # Configuration logs
    if args.verbose and not args.json:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.CRITICAL)
        
    text = args.input
    if not text:
        if args.json:
            print(json.dumps({"error": "Empty input"}))
        else:
            print("Erreur: Entrée vide")
        sys.exit(1)
        
    # Détection langue
    lang = args.lang
    if not lang:
        # Pour détecter, on ne peut pas utiliser le chiffré brut avec des stopwords
        # On devra détecter post-déchiffrement ou utiliser une heuristique.
        # Ici on utilise 'fr' par défaut ou une logique simple.
        # Pour Vigenère/César, l'analyse fréquentielle dépend de la langue.
        # On va essayer de décoder en supposant FR puis EN si le score est mauvais?
        # Pour l'instant on fixe 'fr' par défaut comme demandé implicitement par les TPs classiques.
        lang = 'fr' 
    
    candidates = []
    
    # 1. César
    logging.info("Lancement analyse César...")
    caesar_raw = get_caesar_candidates(text)
    for c in caesar_raw:
        # Scoring enrichi
        metrics = calculate_score(c['plaintext'], lang=lang)
        c['score_final'] = metrics['score']
        c['type'] = 'Caesar'
        c['meta'] = metrics
        candidates.append(c)
        
    # 2. Vigenère
    logging.info("Lancement analyse Vigenère...")
    # On limite Vigenère aux textes assez longs pour Kasiski (> 20 chars disons)
    if len(text) > 10:
        vigenere_cands = crack_vigenere(text, lang=lang)
        candidates.extend(vigenere_cands)
        
    # Tri global
    # Le score de scoring.py est plus élevé = meilleur
    candidates.sort(key=lambda x: x['score_final'], reverse=True)
    
    # Top N
    top_n = candidates[:args.top]
    
    if args.json:
        # Nettoyage pour JSON (pas de sets etc)
        # Mais nos dicts sont simples.
        print(json.dumps(top_n, indent=2, ensure_ascii=False))
    else:
        print(f"--- Top {args.top} Solutions ---")
        for i, cand in enumerate(top_n):
            print(f"#{i+1} [{cand['type']}] Key: {cand['key']}")
            print(f"   Score: {cand['score_final']:.2f}")
            print(f"   Excerpt: {cand['plaintext'][:100]}...")
            print()

if __name__ == "__main__":
    main()
