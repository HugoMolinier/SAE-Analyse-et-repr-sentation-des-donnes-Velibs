import SQL
import mysql.connector
import time

# Connexion à la base de données
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="velibs"
)
# Création du curseur
mycursor = mydb.cursor()

# Création des tables
SQL.creation_table(mycursor)
try:
    SQL.create_trigger(mycursor, mydb)
except:
    # Si le trigger existe déjà on passe
    pass

# Insertion des valeurs dans les tables
SQL.insertion_valeur_fixe(mycursor, SQL.telechargement_donnees_fixe(), mydb)
while True:
    # Insertion des valeurs temporaires dans la table station_status toutes les 10 minutes
    try:
        SQL.insertion_valeur_temporaire(mycursor, SQL.telechargement_donnees_temporaire(), mydb)
    except Exception as e:
        # Une erreur peut se produire si on se déconnecte de la base de données
        print('Erreur', e)
        print('Réessaie dans 10 minutes')
    time.sleep(600)
