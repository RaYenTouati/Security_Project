# 🔐 Outil de Cryptanalyse Automatisé (Caesar & Vigenère)

Cet outil est une solution complète pour l'analyse et le cassage de chiffrements classiques sans connaissance de la clé. Il combine des techniques de cryptanalyse traditionnelles (Kasiski, Indice de Coïncidence) avec une analyse fréquentielle moderne et un scoring linguistique avancé.

## 🚀 Fonctionnalités

### 1. Chiffre de César
*   **Chiffrement/Déchiffrement** : Supporte la casse et la ponctuation.
*   **Brute-force intelligent** : Génère les 25 candidats et identifie automatiquement le meilleur grâce au scoring.

### 2. Chiffre de Vigenère
*   **Cryptanalyse "Zero-Knowledge"** : Retrouve la clé sans aucune information préalable.
*   **Pipeline d'analyse** :
    *   Détection de longueur de clé (Test de Kasiski + Indice de Coïncidence).
    *   Analyse fréquentielle par colonne (Chi-carré).
    *   Reconstitution de la clé et du message clair.

### 3. Analyse & Scoring
*   **Métriques multiples** :
    *   Ratio de mots valides (Dictionnaires FR/EN).
    *   Détection de "Stopwords" (mots vides fréquents).
    *   Entropie de Shannon.
    *   Indice de Coïncidence (IC).
*   **Support multilingue** : Détection et support du Français et de l'Anglais.

### 4. Interface CLI Professionnelle
*   Sortie JSON structurée pour intégration.
*   Mode verbeux pour le débogage.

### 5. Bonus IA 🤖
*   Script d'entraînement (`tools/train_model.py`) pour générer un modèle de Machine Learning (Régression Logistique) capable de classifier un texte comme "chiffré" ou "clair".

---

## 🛠️ Installation

Aucune dépendance externe n'est requise pour le fonctionnement de base (Standard Library Python).

Pour les fonctionnalités avancées (Tests, ML) :
```bash
pip install pytest scikit-learn
```

---

## 💻 Utilisation

Tout se passe via le script principal `bin/crack.py`.

### Casser un code de César
Pour analyser un texte et sortir le meilleur candidat :
```bash
python bin/crack.py --input "VOTRE TEXTE ICI..." --json --top 1
```

### Casser un code de Vigenère
Pour un texte plus complexe (spécifiez la langue pour une meilleure précision) :
```bash
python bin/crack.py --input "TEXTE CHIFFRE VIGENERE" --lang fr
```

### Options disponibles
*   `--input, -i` : Le texte à analyser (obligatoire).
*   `--top, -n` : Nombre de résultats à afficher (défaut: 5).
*   `--json` : Sortie formatée en JSON strict.
*   `--lang, -l` : Langue supposée (`fr` ou `en`).
*   `--verbose, -v` : Affiche les détails de l'exécution.

---

## 📂 Structure du Projet

*   `bin/` : Exécutables et points d'entrée (CLI).
*   `cryptanalysis_tool/` : Le cœur du code.
    *   `ciphers/` : Implémentation des algos (César, Vigenère, Brute-force).
    *   `analysis/` : Logique de scoring, fréquences, preprocessing.
*   `data/` : Ressources linguistiques (listes de mots, stopwords).
*   `tests/` : Tests unitaires automatisés.
*   `tools/` : Outils annexes (Entraînement modèle IA).

---

## 🧪 Tests

Des tests unitaires couvrent l'ensemble des modules.

Lancer tous les tests :
```bash
pytest tests/
```

Lancer le script de vérification simple :
```bash
python verification_test.py
```

---

## 🧠 Détails Techniques

### Scoring Heuristique
Le score final d'un candidat est calculé par une pondération de :
`Score = (Ratio Mots Valides * 50) + (Ratio Stopwords * 100)`
Cela permet de privilégier fortement les phrases grammaticalement correctes.

### Cassage Vigenère
L'algorithme utilise la méthode statistique :
1.  **Kasiski** : Trouve les distances entre séquences répétées pour déduire les diviseurs communs (longueurs de clé probables).
2.  **IC Moyen** : Vérifie quelle longueur donne un Indice de Coïncidence proche de celui de la langue cible (0.074 pour le FR).
3.  **Chi-2** : Pour chaque lettre de la clé, on teste les 26 décalages et on garde celui dont la distribution de fréquence minimise la distance du Chi-carré avec la langue cible.
