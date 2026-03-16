# 🌿 Streamlit Wetlands Explorer

Application web interactive développée avec Streamlit permettant d'explorer une grille de tuiles géographiques et d'afficher les **zones humides** associés à chaque tuile.

**UN POLYGONE REPRESENTE UNE PROBABILITÉ >60% D'OBTENIR UNE ZONE HUMIDE À PARTIR D'UNE APPROCHE MCA**

Utilisation :
- La carte principale affiche la grille des tuiles.
- L'utilisateur clique sur une tuile.
- L'application charge les données géographiques associées et affiche les zones humides.

---

# 📂 Structure du projet
```
streamlit_wetlands_explorer/
│
├─ app.py                 # Code principal Streamlit
├─ requirements.txt       # Librairies Python nécessaires
├─ grid.geojson           # Grille de tuiles GeoJSON
├─ tiles/                 # GeoJSON par tuile (id_1.geojson, id_2.geojson, ...) (wetlands)
└── README.md
```

---

# ⚡ Déploiement rapide

Lancer localement

#### 1. Cloner le dépôt
```
git clone https://github.com/thibaultmenez/streamlit_wetlands_explorer/
cd streamlit_wetlands_explorer
```

#### 2. Installer les dépendances
```
pip install -r requirements.txt
```
#### 3. Lancer l’app
```
streamlit run app.py
```
