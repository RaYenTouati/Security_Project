# cryptanalysis_tool/analysis/vigenere_crack.py

import math
from collections import Counter, defaultdict
from typing import List, Dict, Tuple
from ..ciphers.vigenere import decrypt
from .scoring import calculate_chi_squared, calculate_score, detect_language
from .preprocessing import save_spaces_index, clean_text, restore_spaces
from ..ciphers.caesar import decrypt as caesar_decrypt

def get_sequences(text: str, n: int) -> Dict[str, List[int]]:
    """Trouve les séquences répétées de taille n et leurs positions."""
    sequences = defaultdict(list)
    for i in range(len(text) - n + 1):
        seq = text[i:i+n]
        sequences[seq].append(i)
    
    return {seq: pos for seq, pos in sequences.items() if len(pos) > 1}

def get_sequence_distance(text: str, seq: str) -> List[int]:
    """Retourne les distances entre les occurrences d'une séquence."""
    # Note: L'implémentation précédente utilisait déjà une map, 
    # mais ici on recalculerait ou utiliserait la sortie de get_sequences.
    # Simplification : on suppose que 'text' est déjà le 'cleaned_text'
    pass # Non utilisé directement si on intègre tout dans get_key_length

def get_divisions(n: int) -> List[int]:
    """Retourne les diviseurs de n (excluant 1)."""
    divs = []
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divs.append(i)
            if i * i != n:
                divs.append(n // i)
    divs.append(n)
    return sorted(divs)

def get_key_length(ciphertext: str, max_len=20) -> List[Tuple[int, float]]:
    """
    Estime la longueur de la clé via Kasiski et IC.
    Retourne [(length, score), ...] trié par score.
    """
    cleaned = clean_text(ciphertext)
    
    # 1. Kasiski
    distances = []
    for n in range(3, 6): # Trigrammes à Pentagrammes
        seqs = get_sequences(cleaned, n)
        for positions in seqs.values():
            for i in range(len(positions) - 1):
                dist = positions[i+1] - positions[i]
                distances.append(dist)
    
    candidate_lengths = Counter()
    for d in distances:
        divs = get_divisions(d)
        for div in divs:
            if div <= max_len:
                candidate_lengths[div] += 1
                
    # 2. Indice de Coïncidence (IC)
    # IC moyen théorique pour une longueur L
    ic_scores = {}
    for L in range(1, max_len + 1):
        avg_ic = 0
        for i in range(L):
            subtext = cleaned[i::L]
            if len(subtext) > 1:
                # IC basic calculation
                counts = Counter(subtext)
                N = len(subtext)
                ic = sum(c*(c-1) for c in counts.values()) / (N*(N-1))
                avg_ic += ic
        avg_ic /= L
        ic_scores[L] = avg_ic

    # Fusion des scores
    final_scores = []
    # On cherche un IC proche de 0.074 (Français) ou 0.066 (Anglais)
    # et soutenu par Kasiski
    target_ic = 0.074 
    
    max_kasiski = max(candidate_lengths.values()) if candidate_lengths else 1
    
    for L in range(1, max_len + 1):
        k_score = candidate_lengths.get(L, 0) / max_kasiski
        ic_dist = abs(ic_scores[L] - target_ic)
        # Score inverse de la distance IC (plus c'est proche, mieux c'est)
        ic_score = 1.0 - (ic_dist / 0.04) # Normalisation simple
        if ic_score < 0: ic_score = 0
        
        # Le score global : mix Kasiski et IC
        # Si Kasiski est fort, c'est un très bon signe
        global_score = 0.4 * k_score + 0.6 * ic_score
        final_scores.append((L, global_score, ic_scores[L]))
        
    final_scores.sort(key=lambda x: x[1], reverse=True)
    return final_scores[:5]

def solve_caesar_column(text: str) -> int:
    """Trouve le meilleur shift pour une colonne (César)."""
    best_shift = 0
    best_chi2 = float('inf')
    
    for shift in range(26):
        decrypted = caesar_decrypt(text, shift)
        chi2 = calculate_chi_squared(decrypted)
        if chi2 < best_chi2:
            best_chi2 = chi2
            best_shift = shift
    return best_shift

def crack_vigenere(ciphertext: str, lang='fr') -> List[Dict]:
    """
    Tente de casser Vigenère. Retourne les meilleures solutions.
    """
    cleaned = clean_text(ciphertext)
    spaces = save_spaces_index(ciphertext)
    
    # 1. Trouver longueur clé
    top_lengths = get_key_length(ciphertext)
    
    candidates = []
    
    # On essaie les 3 meilleures longueurs
    for L, score_len, ic_val in top_lengths[:3]:
        key_chars = []
        for i in range(L):
            col_text = cleaned[i::L]
            shift = solve_caesar_column(col_text)
            key_chars.append(chr(ord('A') + shift))
            
        key = "".join(key_chars)
        
        # Déchiffrement
        plaintext_cleaned = decrypt(cleaned, key)
        # Reconstitution (ne marche que si ciphertext avait des espaces/ponct conservés 
        # mais ici decrypt renvoie un texte type "A-Z", on doit réinsérer les espaces du ciphertext original)
        
        # Pour le rendu final, on veut le texte avec espaces. 
        # Notre fonction decrypt dans ciphers/vigenere préserve la ponctuation si on lui passe le texte original.
        # Mais ici on a construit la clé sur le cleaned.
        
        final_plaintext = decrypt(ciphertext, key)
        
        # Scoring global
        metrics = calculate_score(final_plaintext, lang=lang)
        
        candidates.append({
            "type": "Vigenere",
            "key": key,
            "score_final": metrics['score'],
            "plaintext": final_plaintext,
            "meta": {
                "key_length": L,
                "ic": ic_val,
                "metrics": metrics
            }
        })
        
    candidates.sort(key=lambda x: x['score_final'], reverse=True)
    return candidates
