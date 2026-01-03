# tools/train_model.py
import sys
import os
import joblib
import random
try:
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import cross_val_score
    import numpy as np
except ImportError:
    print("scikit-learn not installed. Skipping ML tool.")
    sys.exit(0)

# Ajout du chemin racine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cryptanalysis_tool.ciphers import caesar, vigenere
from cryptanalysis_tool.analysis.scoring import calculate_entropy, calculate_ic, calculate_score

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

def generate_dataset(n_samples=1000):
    # Charge texte
    with open(os.path.join(DATA_DIR, 'sample_plain.txt'), 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f if l.strip()]
        
    X = []
    y = []
    
    for _ in range(n_samples):
        text = random.choice(lines)
        if not text: continue
        
        # 50% chance d'être du texte clair (label 1)
        # 50% chance d'être du chiffré (label 0)
        is_plain = random.random() > 0.5
        
        if is_plain:
            sample = text
            label = 1
        else:
            # Chiffrer
            mode = random.choice(['caesar', 'vigenere'])
            if mode == 'caesar':
                k = random.randint(1, 25)
                sample = caesar.encrypt(text, k)
            else:
                k_len = random.randint(2, 10)
                # key 'ABC...'
                key = "".join(chr(random.randint(65, 90)) for _ in range(k_len))
                sample = vigenere.encrypt(text, key)
            label = 0
            
        # Features
        # On réutilise scoring mais on veut les valeurs brutes pour le ML
        # Entropy, IC, Space ratio (si espaces présents -> indice fort pour clair, mais ici on teste sans espaces peut-etre ?)
        # Le prompt dit "plaintext -> chiffré -> déchiffré toutes clés".
        # Ah, le modèle doit classifier si un CANDIDAT est bon ou pas ? 
        # "labels (1 vrai plaintext, 0 sinon)"
        # Oui c'est ça.
        
        ic = calculate_ic(sample)
        ent = calculate_entropy(sample)
        # On triche un peu en réutilisant le scoring existant pour avoir valid_ratio
        sc = calculate_score(sample)
        valid_ratio = sc['valid_ratio']
        stop_ratio = sc['stop_ratio']
        
        X.append([ic, ent, valid_ratio, stop_ratio])
        y.append(label)
        
    return np.array(X), np.array(y)

def train():
    print("Generating dataset...")
    X, y = generate_dataset()
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    clf = LogisticRegression(class_weight='balanced')
    scores = cross_val_score(clf, X_scaled, y, cv=5, scoring='accuracy')
    
    print(f"CV Accuracy: {scores.mean():.4f}")
    
    clf.fit(X_scaled, y)
    
    output_path = os.path.join(os.path.dirname(__file__), 'caesar_model.joblib')
    joblib.dump({'model': clf, 'scaler': scaler}, output_path)
    print(f"Model saved to {output_path}")

if __name__ == "__main__":
    train()
