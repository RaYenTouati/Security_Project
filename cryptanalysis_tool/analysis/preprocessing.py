# cryptanalysis_tool/analysis/preprocessing.py

from typing import Tuple, List

def save_spaces_index(text: str) -> List[int]:
    """
    Retourne les indices des espaces dans le texte original.
    Peut être étendu pour la ponctuation.
    """
    return [i for i, char in enumerate(text) if char.isspace()]

def clean_text(text: str) -> str:
    """
    Ne garde que les lettres A-Z, convertit en majuscules.
    """
    return "".join(c.upper() for c in text if c.isalpha())

def restore_spaces(cleaned_text: str, space_indices: List[int]) -> str:
    """
    Reconstitue le texte avec les espaces aux positions d'origine.
    Note: Si le texte déchiffré n'a pas la même longueur que le nettoyé (ce qui ne doit pas arriver par substitution), cela plantera.
    On insère les espaces aux bons endroits.
    """
    res = list(cleaned_text)
    for idx in space_indices:
        if idx < len(res) + 1: # +1 car on ajoute
            res.insert(idx, ' ')
        else:
            res.append(' ')
    return "".join(res)
