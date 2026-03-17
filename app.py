import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from folium.plugins import Fullscreen

st.set_page_config(layout="wide")
st.title("Carte interactive des tuiles")



st.sidebar.title("Infos")

st.sidebar.write(f""" 
                
                 ---
                 
Cette application permet de visualiser une carte de probabilité d'obtenir des zones humides > 60%.
Voir detail : https://thibaultmenez.github.io/DinBuam_Wetlands/03.%20DEM%20et%20cartes%20hydro/M%C3%A9thode/
            
🛰️ Source : données GeoJSON (poly wetlands) + google satellite (carte de fond)
            
---

""")

@st.cache_data
def load_grid():
    return gpd.read_file("data/grid.geojson").to_crs("EPSG:4326")

grid = load_grid()

@st.cache_data
def load_tile(tile_id):
    gdf = gpd.read_file(f"data/tiles/id_{tile_id}.geojson")
    return gdf.to_crs("EPSG:4326")

st.subheader(f"Grille de selection")
st.write("Clique sur une tuile pour explorer")
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

st.markdown("""
            ---
            """)
# -------------------------
# détection du clic
# -------------------------
if map_data and map_data.get("last_clicked"):

    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    # trouver la tuile correspondante
    point = gpd.GeoSeries.from_xy([lon], [lat], crs=4326)

    point_geom = point.iloc[0]

    possible_matches = grid[grid.geometry.bounds.apply(
        lambda row: row.minx <= lon <= row.maxx and row.miny <= lat <= row.maxy,
        axis=1
    )]
    selected = possible_matches[possible_matches.contains(point_geom)]

    if len(selected) > 0:

        tile_id = selected.iloc[0]["id"]
        st.subheader(f"Tuile sélectionnée : id {tile_id}")


        # charger les polygones de la tuile
        with st.spinner("Chargement de la tuile..."):
            gdf = load_tile(tile_id)
            gdf_proj = gdf.to_crs(epsg=3857)  # projection métrique
            surface_totale = gdf_proj.area.sum() / 1e6  # en km²

        st.write(f"Surface totale : {surface_totale:.2f} km²")

        # nouvelle carte zoomée
        m2 = folium.Map(location=[lat, lon], zoom_start=14)

        # définir le style AVANT
        def style_function(feature):
            area = feature["properties"].get("area", 0)
            return {
                "fillColor": "red" if area > 1 else "yellow",
                "color": "black",
                "weight": 1,
                "fillOpacity": 0.5,
            }

        # afficher les polygones
        folium.GeoJson(
            gdf,
            style_function=style_function,
            smooth_factor=1
        ).add_to(m2)
        folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
            attr="Google",
            name="Google Satellite"
        ).add_to(m2)
        # bouton plein écran
        Fullscreen(
            position="topleft",
            title="Plein écran",
            title_cancel="Quitter plein écran",
            force_separate_button=True
        ).add_to(m2)
        st_folium(m2, width=700, height=500)
        st.markdown("🟨 Polygones de la tuile sélectionnée")
