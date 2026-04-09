# 🎵 Taylor Swift Lyrics Generator — LSTM & Full-Stack Web App

Génération automatique de paroles de chansons dans le style de Taylor Swift utilisant un réseau de neurones récurrents (**LSTM**) et une interface web moderne avec système d'authentification.

![Swiftie AI Banner](https://img.shields.io/badge/Model-LSTM-pink?style=for-the-badge&logo=keras)
![Stack](https://img.shields.io/badge/Stack-Flask_%7C_MySQL_%7C_TensorFlow-blue?style=for-the-badge)

---

## 📌 Présentation du Projet

Ce projet a évolué d'un simple générateur de texte vers une plateforme web complète. Il permet aux utilisateurs de :
1. **Découvrir** la technologie derrière la génération de paroles.
2. **S'inscrire et se connecter** via un système sécurisé.
3. **Générer des paroles** uniques basées sur des modèles linguistiques entraînés sur la discographie de Taylor Swift (jusqu'à *Reputation*).

### Nouvelles Fonctionnalités :
- **Authentification complète** : Inscription, Connexion, Déconnexion avec mots de passe hachés.
- **Interface Multi-pages** :
  - `Accueil` : Présentation du service.
  - `Technologie` : Détails sur l'architecture LSTM.
  - `Processus` : Comment fonctionne l'entraînement.
  - `Prix` : Structure de l'offre (simulée).
- **Base de données MySQL** : Gestion persistante des utilisateurs.

---

## 🛠️ Installation et Configuration (Pour l'équipe)

### 1. Prérequis
- Python 3.9+
- Serveur MySQL (XAMPP recommandé pour Windows)
- Port MySQL par défaut : `3307` (ou modifier dans `app.py`)

### 2. Configuration de la Base de Données
Exécutez le script SQL fourni pour créer la structure :
1. Ouvrez **phpMyAdmin** ou votre client SQL.
2. Importez le fichier [`setup_db.sql`](file:///c:/Users/OUALI/lstm_project/setup_db.sql).
3. Cela créera la base `taylor_db` et la table `users`.

### 3. Installation des Dépendances
```bash
pip install flask flask-mysqldb numpy tensorflow keras scikit-learn pandas
```

### 4. Lancement de l'Application
```bash
python app.py
```
L'application sera disponible sur `http://127.0.0.1:5000`.

---

## 📁 Structure du Projet

```text
lstm_project/
│
├── app.py                    # Serveur Flask (Routes, Auth, Inférence)
├── setup_db.sql              # Script d'initialisation MySQL
├── taylor_swift_lstm.keras   # Modèle LSTM entraîné
├── tokenizer.pkl             # Vocabulaire sauvegardé
│
├── templates/                # Pages HTML (Jinja2)
│   ├── home.html             # Landing page
│   ├── login.html            # Connexion
│   ├── register.html         # Inscription
│   ├── index.html            # Générateur (Protégé)
│   └── ...                   # Autres pages statiques
│
└── lstm_taylor_swift.ipynb   # Notebook de recherche & entraînement
```

---

## 🧠 Détails Techniques

- **Modèle** : LSTM multicouche (150 + 100 unités).
- **Frontend** : HTML5/CSS3 avec design premium (Glassmorphism & animations).
- **Backend** : Flask avec sessions sécurisées et `flask-mysqldb`.

---

## 📜 Licence
Ce projet est destiné à des fins éducatives. Les paroles originales appartiennent à Taylor Swift.