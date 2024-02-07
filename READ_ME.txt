Crée par MOLINIER Hugo
Groupe B2

modules utilisés:
	- mysql.connector
	- time
	- requests
	- pandas
	- datetime
	- folium
	- folium.plugins
	- json
	- numpy
	- flask

=========================


Détails :
Pour Insertion des données dans la base de donnée aussi création des tables et triggers: Insertion_valeur.py
Lancement de l'application web sous flask: main.py
Création des graphiques: Analyse.py
Les commandes SQL/récolte donnée: SQL.py
Création de la carte sous folium: creation_carte.py
La structure de la base de données: velibs.sql




==========================


Précision:
Pour pouvoir lancé main.py il faut que le serveur oû mysql.connector soit allumé
Après avoir lancé main.py, le site web se trouvera a l'adresse suivante: http://127.0.0.1:5000/
La carte est sauvegarder dans ./static/carte.html
Les images des graphiques générées par l'application web se situe dans le dossier ./static/graphique
On peut voir certain exemple de graphique en lancant en temps que programme principal Analyse.py
C'est graphique ne seront pas sauvagarder en temps qu'image mais s'afficheront juste
Vous pouvez crée une carte sans lancer le programme main.py en executant carte.py en module principal.
mysql.connector se connecte à:
    host="localhost"
    user="root"
    database="velibs"
