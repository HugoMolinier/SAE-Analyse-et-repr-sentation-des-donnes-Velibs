import folium
from folium.plugins import MarkerCluster
import mysql.connector
import json
import pandas
import SQL
import numpy as np


# Connexion à la base de données
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="velibs"
)
# Création du curseur
mycursor = mydb.cursor()
def creation_carte_paris():
    # Récupérer les données de la carte de Paris pour afficher un tracer
    with open('./static/arrondissements.geojson') as f:
        parisloc= json.load(f)

    # Créer une carte folium
    my_map = folium.Map(location=[48.8566, 2.3522], zoom_start=11,titles="Map Station Velibs")

    # Ajouter un marqueur à la carte
    mCluster = MarkerCluster(name="Affichage Station",disableClusteringAtZoom=15).add_to(my_map)

    # Ajouter une couche GeoJSON à la carte
    folium.GeoJson(parisloc,name="Paris Departments").add_to(my_map)

    data = SQL.select_table(mycursor, 'station_information', 'station_information.stationcode,station_information.name,station_information.capacity,station_status.numdocksavailable,station_status.numbikesavailable,station_status.mechanical,station_status.ebike,station_information.lat,station_information.lon,station_status.is_installed',"INNER JOIN station_status ON station_information.stationcode = station_status.stationcode WHERE (station_status.stationcode, station_status.date_insertion) IN (SELECT stationcode, MAX(date_insertion) FROM station_status GROUP BY stationcode) ")
    data=data[['stationcode','name','capacity','numdocksavailable','numbikesavailable','mechanical','ebike','lat','lon','is_installed']]
    for i, row in data.iterrows():
        #Pour chaque station on ajoute un marqueur sur la carte avec les informations de la station en popup
        # et une couleur en fonction de l'état de la station
        if row['is_installed'] == 0:
            color='red'
        elif row['numbikesavailable'] == 0:
            color='orange'
        else:
            color='blue'
        # Créer un popup pour chaque station
        val=(row['name'],row['capacity'],row['numdocksavailable'],row['mechanical'],row['ebike'],row['stationcode'])
        popup = '''<div style="white-space: nowrap; fit-content(100); overflow: normal; word-wrap: break-word; text-align: left;padding: 2px;"><h4> %s </h4><p style="font-size: 14px; padding:3px;">Capacité: %s <br>Places disponibles: %s <br>Vélos méquanique: %s <br>Vélos éléctriques: %s <br>Code: %s</p></div>'''
        popups = popup % val
        # Ajouter un marqueur à la carte
        folium.Marker([row['lat'], row['lon']], popup=popups,max_width=10,icon=folium.Icon(icon="bicycle", prefix="fa",color=color), max_zoom=14, min_zoom=20).add_to(mCluster)

    # Ajouter un controleur de couche à la carte pour réunir les différentes couches(les cercles)
    folium.LayerControl().add_to(my_map)

    my_map.save('./static/carte.html')
    return

if __name__ == '__main__':
    """Lance la création de la carte de Paris"""
    creation_carte_paris()
    print('Carte générée')