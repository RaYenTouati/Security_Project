from typing import Dict, Set

"""
Données linguistiques pour la cryptanalyse du français.
Inclut les fréquences des lettres, les bigrammes et un dictionnaire de mots courants.
"""

# Fréquences des lettres en français (en pourcentage, source standard)
# Total ~ 100%
FRENCH_LETTER_FREQUENCIES: Dict[str, float] = {
    'A': 7.636, 'B': 0.901, 'C': 3.260, 'D': 3.669, 'E': 14.715,
    'F': 1.066, 'G': 0.866, 'H': 0.737, 'I': 7.529, 'J': 0.545,
    'K': 0.049, 'L': 5.456, 'M': 2.968, 'N': 7.095, 'O': 5.378,
    'P': 3.021, 'Q': 1.362, 'R': 6.553, 'S': 7.948, 'T': 7.244,
    'U': 6.311, 'V': 1.628, 'W': 0.114, 'X': 0.387, 'Y': 0.308, 'Z': 0.136
}

# Fréquences des bigrammes les plus courants (Source indicative)
# Utile pour affiner l'analyse si les lettres seules ne suffisent pas.
FRENCH_BIGRAMS: Dict[str, float] = {
    'ES': 3.15, 'LE': 2.22, 'DE': 2.18, 'RE': 2.10, 'EN': 2.08,
    'ON': 1.64, 'NT': 1.60, 'TE': 1.55, 'NE': 1.43, 'AI': 1.38,
    'SE': 1.35, 'IT': 1.32, 'ME': 1.28, 'ER': 1.25, 'OU': 1.23,
    'QU': 1.20, 'AN': 1.15, 'DA': 1.10, 'ST': 1.05, 'US': 1.00
}

# Liste de mots très courants en français pour le scoring par dictionnaire
# Cette liste permet de valider rapidement si un texte déchiffré a du sens.
COMMON_FRENCH_WORDS: Set[str] = {
    # Articles / Prépositions / Conjonctions
    "LE", "LA", "LES", "UN", "UNE", "DES", "DU", "AU", "AUX",
    "DE", "A", "EN", "PAR", "POUR", "DANS", "SUR", "AVEC", "SANS", "SOUS",
    "ET", "OU", "MAIS", "DONC", "OR", "NI", "CAR", "QUE", "SI", "COMME",
    
    # Pronoms
    "JE", "TU", "IL", "ELLE", "ON", "NOUS", "VOUS", "ILS", "ELLES",
    "ME", "TE", "SE", "Lui", "LEUR", "Y", "EN", "QUI", "QUE", "DONT", "OU",
    "CE", "CET", "CETTE", "CES", "CELA", "CA",
    "MON", "TON", "SON", "MA", "TA", "SA", "MES", "TES", "SES", "NOTRE", "VOTRE", "J", "M", "T", "S", "L", "D", "N",

    # Verbes courants (Etre, Avoir, Faire, etc. conjugués)
    "EST", "SONT", "SUIS", "ES", "SOMMES", "ETES", "ETRE", "ETE",
    "AI", "AS", "A", "AVONS", "AVEZ", "ONT", "AVOIR", "EU",
    "FAIT", "FAIRE", "FONT", "DIRE", "DIT", "ALLER", "VAIS", "VA", "VONT",
    "POUVOIR", "PEUX", "PEUT", "PEUVENT", "VOULOIR", "VEUX", "VEUT", "VEULENT",
    "DEVOIR", "DOIS", "DOIT", "DOIVENT", "FALLOIR", "FAUT",
    "SAVOIR", "SAIS", "SAIT", "SAVENT", "VOIR", "VOIT", "VOIENT",
    "MANGER", "PRENDRE", "DONNER", "PARLER", "METTRE", "PASSER",
    
    # Adverbes / Autres
    "PAS", "PLUS", "MOINS", "TRES", "BIEN", "MAL", "PEU", "BEAUCOUP",
    "TOUT", "TOUTE", "TOUS", "TOUTES", "MEME", "AUTRE",
    "ICI", "LA", "AILLEURS", "MAINTENANT", "ALORS", "APRES", "AVANT", "JAMAIS", "TOUJOURS",
    "OUI", "NON", "MERCI", "BONJOUR",
    
    # Noms communs fréquents
    "TEMPS", "JOUR", "ANNEE", "VIE", "MONDE", "HOMME", "FEMME", "ENFANT",
    "FRANCE", "PARIS", "CHOSE", "MOMENT", "FOIS", "PETIT", "GRAND", "BON", "MAUVAIS"
}
