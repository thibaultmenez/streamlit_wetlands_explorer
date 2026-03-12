🌿 Streamlit Wetlands Explorer

Une application interactive pour visualiser et explorer les zones humides (wetlands) découpées en tuiles sur une carte satellite.
L’utilisateur peut :
- Visualiser une grille de tuiles sur la carte.
- Cliquer sur une tuile pour zoomer et afficher les polygones de wetlands correspondants.
- Naviguer facilement grâce à l’option plein écran.

---

📂 Structure du projet
streamlit_wetlands/
│
├─ app.py                 # Code principal Streamlit
├─ requirements.txt       # Librairies Python nécessaires
├─ runtime.txt            # Version Python pour Streamlit Cloud
├─ grid.geojson           # Grille de tuiles GeoJSON
├─ tiles/                 # GeoJSON par tuile (id_001.geojson, id_002.geojson, ...)

---

⚡ Déploiement rapide

Lancer localement

# 1. Cloner le dépôt
```
git clone https://github.com/tonusername/streamlit_wetlands.git
cd streamlit_wetlands
```

# 2. Installer les dépendances
```
pip install -r requirements.txt
```
# 3. Lancer l’app
```
streamlit run app.py
```
