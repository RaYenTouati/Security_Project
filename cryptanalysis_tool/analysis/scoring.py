# cryptanalysis_tool/analysis/scoring.py

import math
import os
from collections import Counter
from typing import Dict, Any, List
import re

# Constantes de chemins
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')

def load_words(lang: str) -> set:
    try:
        path = os.path.join(DATA_DIR, f'words_{lang}.txt')
        with open(path, 'r', encoding='utf-8') as f:
            return set(w.strip().upper() for w in f)
    except FileNotFoundError:
        return set()

def load_stopwords(lang: str) -> set:
    try:
        path = os.path.join(DATA_DIR, f'stopwords_{lang}.txt')
        with open(path, 'r', encoding='utf-8') as f:
            return set(w.strip().lower() for w in f) # stopwords souvent en minuscule
    except FileNotFoundError:
        return set()

# Chargement global (pour l'instant lazy loading ou init explicite recommandé, mais on fait simple)
WORDS_FR = load_words('fr')
WORDS_EN = load_words('en')
STOPWORDS_FR = load_stopwords('fr')
STOPWORDS_EN = load_stopwords('en')

# Fréquences théoriques (simplifiées)
FRENCH_LETTER_FREQUENCIES = {
    'E': 14.7, 'A': 7.6, 'I': 7.5, 'S': 7.9, 'N': 7.1, 'R': 6.6, 'T': 7.2, 'O': 5.4, 'L': 5.5, 'U': 6.3,
    'D': 3.7, 'C': 3.3, 'M': 3.0, 'P': 3.0, 'G': 0.9, 'B': 0.9, 'V': 1.6, 'H': 0.7, 'F': 1.1, 'Q': 1.4,
    'Y': 0.3, 'X': 0.4, 'J': 0.5, 'K': 0.05, 'W': 0.1, 'Z': 0.1
}

def calculate_entropy(text: str) -> float:
    """Calcule l'entropie de Shannon du texte."""
    if not text:
        return 0.0
    text = text.upper()
    counts = Counter(text)
    length = len(text)
    entropy = 0.0
    for count in counts.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy

def calculate_ic(text: str) -> float:
    """Indice de coïncidence."""
    text = [c for c in text.upper() if c.isalpha()]
    n = len(text)
    if n <= 1:
        return 0.0
    counts = Counter(text)
    numerator = sum(c * (c - 1) for c in counts.values())
    return numerator / (n * (n - 1))

def detect_language(text: str) -> str:
    """
    Détecte la langue (fr ou en) basée sur les stopwords.
    """
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    if not words:
        return 'fr' # Default
    
    score_fr = sum(1 for w in words if w in STOPWORDS_FR)
    score_en = sum(1 for w in words if w in STOPWORDS_EN)
    
    return 'fr' if score_fr >= score_en else 'en'

def calculate_chi_squared(text: str, lang='fr') -> float:
    """
    Calcule le Chi-deux de frequence de lettres.
    """
    text = "".join(c for c in text.upper() if c.isalpha())
    length = len(text)
    if length == 0:
        return float('inf')
        
    counts = Counter(text)
    chi2 = 0.0
    
    # On utilise les fréquences françaises par défaut pour l'instant
    # Idéalement on chargerait ENGLISH_LETTER_FREQUENCIES si lang='en'
    ref_freqs = FRENCH_LETTER_FREQUENCIES
    
    for char, freq_percent in ref_freqs.items():
        observed = counts.get(char, 0)
        expected = (freq_percent / 100) * length
        chi2 += ((observed - expected) ** 2) / expected
        
    return chi2

def calculate_score(text: str, lang: str = 'fr') -> Dict[str, Any]:
    """
    Calcule un score complet pour le texte candidat.
    """
    words_ref = WORDS_FR if lang == 'fr' else WORDS_EN
    
    # Nettoyage
    words = re.findall(r'\b\w+\b', text.upper())
    total_words = len(words)
    
    valid_word_count = sum(1 for w in words if w in words_ref)
    valid_ratio = valid_word_count / total_words if total_words > 0 else 0
    
    stop_ref = STOPWORDS_FR if lang == 'fr' else STOPWORDS_EN
    words_lower = [w.lower() for w in words]
    stop_count = sum(1 for w in words_lower if w in stop_ref)
    stop_ratio = stop_count / total_words if total_words > 0 else 0
    
    entropy = calculate_entropy(text)
    ic = calculate_ic(text)
    
    # Heuristique combinée:
    # On donne beaucoup de poids aux stopwords et mots valides
    # Un texte français a une entropie autour de 4.0-4.5 (lettres) mais ici c'est brut
    # IC français ~ 0.074, Random ~ 0.038
    
    score = (valid_ratio * 50) + (stop_ratio * 100)
    
    return {
        "score": score,
        "valid_ratio": valid_ratio,
        "stop_ratio": stop_ratio,
        "entropy": entropy,
        "ic": ic,
        "lang": lang
    }
