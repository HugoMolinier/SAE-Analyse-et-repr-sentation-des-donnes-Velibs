import requests
import pandas as pd
import mysql.connector
from datetime import datetime


def telechargement_donnees_fixe():
    """ void -> DataFrame
    Cette fonction permet de télécharger les données fixes
    de disponibilité des vélos en temps réel"""
    try:
        resp = requests.get('https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-emplacement-des-stations/exports/json?lang=fr&timezone=Europe%2FBerlin')
        data = resp.json()
        df = pd.DataFrame(data)
        return df
    except:
        # Si une erreur se produit on renvoie un dataframe vide
        return pd.DataFrame()


def telechargement_donnees_temporaire():
    """ void -> DataFrame
    Cette fonction permet de télécharger les données temporaires
    de disponibilité des vélos en temps réel"""
    try:
        resp = requests.get(
            'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/exports/json?lang=fr&timezone=Europe%2FBerlin')
        data = resp.json()
        df = pd.DataFrame(data)
        df = df.drop(['name', 'capacity', 'is_renting', 'is_returning', 'duedate', 'coordonnees_geo', 'code_insee_commune'], axis=1)
        return df
    except:
        # Si une erreur se produit on renvoie un dataframe vide
        return pd.DataFrame()


def creation_table(mycursor):
    """ cursor -> void
    Cette fonction permet de créer les tables dans la base de données"""
    mycursor.execute("CREATE TABLE IF NOT EXISTS station_information (stationcode VARCHAR(30) PRIMARY KEY NOT NULL, name VARCHAR(255), capacity INT, lon VARCHAR(120),lat VARCHAR(120))")
    mycursor.execute("CREATE TABLE IF NOT EXISTS station_status (stationcode VARCHAR(30) , is_installed TINYINT, numdocksavailable INT, numbikesavailable INT, mechanical INT, ebike INT, nom_arrondissement_communes VARCHAR(255),date_insertion datetime, FOREIGN KEY (stationcode) REFERENCES station_information(stationcode),CONSTRAINT ID_STATION PRIMARY KEY (stationcode,date_insertion))")
    print("Succès de la création des tables")


def insertion_valeur_fixe(mycursor, dataframe, mydb):
    """ cursor,dataframe -> void
    Cette fonction permet d'insérer les valeurs dans la table station_information"""
    sql = """INSERT IGNORE INTO station_information (stationcode, name, capacity, lon,lat) VALUES (%s, %s, %s, %s, %s)"""
    for i in range(len(dataframe)):
        val = (str(dataframe.iloc[i]['stationcode']), dataframe.iloc[i]['name'], int(dataframe.iloc[i]['capacity']),
               str(dataframe.iloc[i]['coordonnees_geo']['lon']),str(dataframe.iloc[i]['coordonnees_geo']['lat']))
        mycursor.execute(sql, val)
    print("Succès de l'insertion des valeurs dans la table station_information")
    mydb.commit()


def insertion_valeur_temporaire(mycursor, dataframe,mydb):
    """cursor,dataframe -> void
    Cette fonction permet d'insérer les valeurs temporaires dans la table station_status"""
    sql = """INSERT INTO station_status (stationcode, is_installed, numdocksavailable, numbikesavailable, mechanical, ebike, nom_arrondissement_communes, date_insertion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    for i in range(len(dataframe)):
        val = (str(dataframe.iloc[i]['stationcode']),dataframe.iloc[i]['is_installed'].replace('OUI', '1').replace('NON', '0'),int(dataframe.iloc[i]['numdocksavailable']), int(dataframe.iloc[i]['numbikesavailable']),int(dataframe.iloc[i]['mechanical']), int(dataframe.iloc[i]['ebike']),dataframe.iloc[i]['nom_arrondissement_communes'], datetime.now())
        mycursor.execute(sql, val)
    print("Succès de l'insertion des valeurs dans la table station_information à la date : ", datetime.now())
    mydb.commit()


def create_trigger(mycursor,mydb):
    """cursor -> void
    Cette fonction permet de créer un trigger qui permet d'ajouter au log dans une table
    supplémentaire, nommée "history_change", les modifications apportées à la table station_status et station_information"""
    mycursor.execute("CREATE TABLE IF NOT EXISTS history_change (user VARCHAR(255), date_insertion datetime ,table_names VARCHAR(255), action VARCHAR(255),station_code VARCHAR(30),FOREIGN KEY (station_code) REFERENCES station_information (stationcode))")
    # trigger table station_status
    mycursor.execute("""CREATE TRIGGER history_insert_station_status AFTER INSERT ON station_status FOR EACH ROW INSERT INTO history_change (user, date_insertion, table_names, action, station_code) VALUES (user(), now(), 'station_status', 'insertion', NEW.stationcode)""")
    mycursor.execute("""CREATE TRIGGER history_update_station_status AFTER UPDATE ON station_status FOR EACH ROW INSERT INTO history_change (user, date_insertion, table_names, action, station_code) VALUES (user(), now(), 'station_status', 'update', NEW.stationcode)""")
    mycursor.execute("""CREATE TRIGGER history_delete_station_status AFTER DELETE ON station_status FOR EACH ROW INSERT INTO history_change (user, date_insertion, table_names, action, station_code) VALUES (user(), now(), 'station_status', 'delete', OLD.stationcode)""")
    # trigger table station_information"""
    mycursor.execute("CREATE TRIGGER history_insert_station_information AFTER INSERT ON station_information FOR EACH ROW INSERT INTO history_change (user, date_insertion, table_names, action, station_code) VALUES (user(), now(), 'station_information', 'insertion', NEW.stationcode)")
    mycursor.execute("CREATE TRIGGER history_update_station_information AFTER UPDATE ON station_information FOR EACH ROW INSERT INTO history_change (user, date_insertion, table_names, action, station_code) VALUES (user(), now(), 'station_information', 'update', NEW.stationcode)")
    mycursor.execute("CREATE TRIGGER history_delete_station_information AFTER DELETE ON station_information FOR EACH ROW INSERT INTO history_change (user, date_insertion, table_names, action, station_code) VALUES (user(), now(), 'station_information', 'delete', OLD.stationcode)")
    print('Succès de la création du trigger')
    mydb.commit()

def select_table(mycursor,table,values="*",condintionsup=""):
    """cursor -> void
    Cette fonction permet de sélectionner les données de la table station_information"""
    try:
        mycursor.execute("SELECT "+values+" FROM "+table+" "+condintionsup)
        myresult = mycursor.fetchall()
        return pd.DataFrame(myresult,columns=[i[0] for i in mycursor.description])
    except:
        print("Erreur de la sélection des données de la table:",table,"| Valeurs :",(values))
        return None

