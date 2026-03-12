import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from folium.plugins import Fullscreen

st.title("Carte interactive des tuiles")

# charger la grille
grid = gpd.read_file("grid.geojson")
grid = grid.to_crs("EPSG:4326")

center = [
    grid.geometry.centroid.y.mean(),
    grid.geometry.centroid.x.mean()
]

m = folium.Map(location=center, zoom_start=8)

# couche grille interactive
folium.GeoJson(
    grid,
    style_function=lambda x: {
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.05
    },
    highlight_function=lambda x: {
        "color": "red",
        "weight": 3,
        "fillOpacity": 0.2
    },
).add_to(m)
folium.TileLayer(
    tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
    attr="Google",
    name="Google Satellite"
).add_to(m)
# afficher la carte
map_data = st_folium(m, width=700, height=500)

# -------------------------
# détection du clic
# -------------------------
if map_data["last_clicked"]:

    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    # trouver la tuile correspondante
    point = gpd.GeoSeries.from_xy([lon], [lat], crs=4326)

    selected = grid[grid.contains(point.iloc[0])]

    if len(selected) > 0:

        tile_id = selected.iloc[0]["id"]

        st.write(f"Tuile sélectionnée : {tile_id}")

        # charger les polygones de la tuile
        gdf = gpd.read_file(f"tiles/id_{tile_id}.geojson")
        gdf = gdf.to_crs("EPSG:4326")

        # nouvelle carte zoomée
        m2 = folium.Map(location=[lat, lon], zoom_start=14)

        # afficher les polygones
        folium.GeoJson(
            gdf,
            style_function=lambda x: {
                "fillColor": "#ffea00",   # couleur
                "color": "black",         # bordure
                "weight": 2,              # épaisseur bordure
                "fillOpacity": 0.5,
            },
            smooth_factor=1
        ).add_to(m2)
        folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
            attr="Google",
            name="Google Satellite"
        ).add_to(m2)
        # bouton plein écran
        Fullscreen(
            position="topright",
            title="Plein écran",
            title_cancel="Quitter plein écran",
            force_separate_button=True
        ).add_to(m2)
        st_folium(m2, width=700, height=500)