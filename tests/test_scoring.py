# tests/test_scoring.py
import pytest
from cryptanalysis_tool.analysis.scoring import calculate_score, calculate_entropy, calculate_ic

def test_scoring_discrimination():
    # Un texte clair doit avoir un meilleur score qu'un texte aléatoire
    plain = "CECI EST UN TEXTE FRANCAIS TOUT A FAIT NORMAL"
    garbage = "XKJQ ZKWJ QLZK JQZL KQZJ ZQKJ QZLK JQZK"
    
    score_plain = calculate_score(plain, 'fr')['score']
    score_garbage = calculate_score(garbage, 'fr')['score']
    
    assert score_plain > score_garbage

def test_entropy():
    # AAAA a entropie nulle
    assert calculate_entropy("AAAA") == 0.0
    # ABCD a entropie plus haute
    assert calculate_entropy("ABCD") > 0.0

def test_ic():
    # AAAA a IC = 1.0 (ou proche selon formule, ici n*(n-1))
    # N=4. Num = 4*3 = 12. Denom = 4*3 = 12. => IC = 1.0
    assert calculate_ic("AAAA") == 1.0
    # ABCD => IC = 0.0
    assert calculate_ic("ABCD") == 0.0
