# ReadMe
## Créateur
Ce projet a été créé par MOLINIER Hugo, dans le cadre du groupe B2.

## Modules Utilisés
-mysql.connector
-time
-requests
-pandas
-datetime
-folium
-folium.plugins
-json
-numpy
-flask

## Détails
### Fichiers et Utilisation
Insertion_valeur.py: Utilisé pour l'insertion des données dans la base de données ainsi que la création des tables et des déclencheurs.
main.py: Permet de lancer l'application web sous Flask.
Analyse.py: Utilisé pour la création des graphiques.
SQL.py: Contient les commandes SQL et la récolte des données.
creation_carte.py: Utilisé pour la création de la carte sous Folium.
velibs.sql: Contient la structure de la base de données.
### Précisions
Pour lancer main.py, assurez-vous que le serveur où mysql.connector est actif.
Après avoir lancé main.py, le site web sera disponible à l'adresse suivante : http://127.0.0.1:5000/
La carte est sauvegardée dans ./static/carte.html.
Les images des graphiques générées par l'application web se trouvent dans le dossier ./static/graphique.
Vous pouvez voir certains exemples de graphiques en exécutant Analyse.py en tant que programme principal. Ces graphiques ne seront pas sauvegardés en tant qu'image mais s'afficheront simplement.
Vous pouvez créer une carte sans lancer le programme main.py en exécutant carte.py en tant que module principal.
mysql.connector se connecte à :
host="localhost"
user="root"
database="velibs"
