import SQL
import mysql.connector
import time
if __name__ != "__main__":
    """Si le fichier n'est pas exécuté directement
    Pour empêcher l'affichage d'erreur dans le terminal lors du programme principal"""
    import matplotlib
    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def analyse_par_station_éléc_méca(nombre_station,boolean, date_debut=(datetime.now()- timedelta(weeks=2)).strftime("%Y-%m-%d %H:%M:%S"), date_fin=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
    """int,boolean,date,date -> None
    Préconditions : La station doit exister
    Rôle : Affiche le nombre de vélos mécanique et électrique à la station en fonction du temps en forme de graphique
    Postconditions : Affiche le graphique en point"""
    df = SQL.select_table(mycursor, "station_status", "*", "WHERE stationcode LIKE '{}' AND date_insertion BETWEEN date('{}') AND date('{}')".format(nombre_station, date_debut, date_fin))
    plt.plot(df['date_insertion'], df['mechanical'], '-*', label='Nombre de vélos mécaniques disponibles')
    plt.plot(df['date_insertion'], df['ebike'], '-*', label='Nombre de vélos électriques disponibles')
    plt.gca().xaxis.set_tick_params(labelsize=7)
    plt.grid(which='major', axis='x', color='black', linestyle='dashed')
    plt.grid(which='major', axis='y', color='black', linestyle='dashed')
    plt.xlabel('Date')
    plt.legend()
    plt.title('Nombre de vélos disponibles à la station ' + str(nombre_station) +'('+date_debut[:10]+' - '+date_fin[:10]+')' )
    if boolean:
        plt.show()
    else:
        plt.savefig('./static/graphique/analyse_par_station_éléc_méca.png')
    plt.close()

def analyse_par_station_dock_available(nombre_station,boolean, date_debut=(datetime.now()- timedelta(weeks=2)).strftime("%Y-%m-%d %H:%M:%S"), date_fin=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
    """int,boolean -> None
    Préconditions : La station doit exister
    Rôle : Affiche le nombre de bornes disponible et des vélos disponibles à la station actuellement
    Postconditions : Affiche le graphique camembert"""
    # Récupérer les données
    df = SQL.select_table(mycursor, "station_status", "AVG(numdocksavailable),AVG(mechanical),AVG(ebike)", "WHERE stationcode LIKE '{}' AND date_insertion BETWEEN date('{}') AND date('{}')".format(nombre_station, date_debut, date_fin))
    numdocksavailable = df['AVG(numdocksavailable)'][0]
    mechanical = df['AVG(mechanical)'][0]
    ebike = df['AVG(ebike)'][0]
    # Créer les labels pour le graphique
    labels = ['Bornes disponibles', 'Vélos mécaniques disponibles', 'Vélos électriques disponibles']

    # Créer les valeurs pour le graphique
    sizes = [numdocksavailable, mechanical , ebike]
    # Créer le graphique
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,colors=['#6388b4', '#57ad8a', '#f2cf5b'])
    plt.title('Répartition des bornes et vélos disponibles actuellement station ' + str(nombre_station)+"\n("+date_debut[:10]+' - '+date_fin[:10]+')')
    if boolean:
        plt.show()
    else:
        plt.savefig('./static/graphique/analyse_par_station_dock_available.png')
    plt.close()



def analyse_par_region_vélo_élec_méca(limite,boolean, date_debut=(datetime.now()- timedelta(weeks=2)).strftime("%Y-%m-%d"), date_fin=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
    """int,date_début,date_fin -> None
    Préconditions : La station doit exister
    Rôle : Affiche le nombre de vélos électrique et mécaniques pour les régions à la station en fonction du temps en forme de graphique
    Postconditions : Affiche le graphique en forme de cammenbert"""
    # Récupérer les données des regions
    myresultregion = SQL.select_table(mycursor, "station_status", "nom_arrondissement_communes,Count(DISTINCT stationcode)", "WHERE date_insertion BETWEEN date('" + date_debut + "') AND date('" + date_fin + "') GROUP BY nom_arrondissement_communes ORDER BY COUNT(DISTINCT stationcode) DESC LIMIT " + str(limite))
    for region in myresultregion['nom_arrondissement_communes']:
        # Fait une requete pour les valeurs pour le graphique
        df = pd.DataFrame(SQL.select_table(mycursor, 'station_status', 'mechanical,ebike', "WHERE nom_arrondissement_communes LIKE '" + region + "'"))
        plt.pie(df.mean(), labels=['Vélo mécanique', 'Vélo éléctrique'], colors=['#6388b4', '#57ad8a'],
                autopct='%1.1f%%', shadow=True, startangle=140)
        plt.title('Répartition des vélos disponibles par type à ' + region+  '\n('+date_debut[:10]+' - '+date_fin[:10]+')')
        if boolean:
            plt.show()
        else:
            plt.savefig('./static/graphique/analyse_par_region_'+region+'.png')
        plt.close()


def analyse_global_éléc_méca(boolean,ordre='DESC',date_debut=(datetime.now()- timedelta(weeks=2)).strftime("%Y-%m-%d"), date_fin=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
    """boolean,String,date,date -> None
    Préconditions : La station doit exister
    Rôle : Affiche le nombre de vélos électrique et mécaniques en fonction du temps en forme de graphique
    Analyse la répartition de vélo électrique et mécaniques dans les 10 communes les plus peuplées ou moins peuplées en station
    Postconditions : Affiche le graphique en histogramme"""
    # Récupérer les données
    df = SQL.select_table(mycursor, 'station_status', 'AVG(mechanical),AVG(ebike),nom_arrondissement_communes', "WHERE is_installed = 1 AND date_insertion BETWEEN date('" + date_debut + "') AND date('" + date_fin + "') GROUP BY nom_arrondissement_communes ORDER BY COUNT(DISTINCT stationcode) "+ordre+" LIMIT 10 ;")
    fig, ax = plt.subplots()
    x_pos = np.arange(len(df))
    # vélos mécaniques
    ax.bar(x_pos - 0.2, df['AVG(mechanical)'], color='blue', alpha=0.5, label='Mécanique', width=0.4, align='center')
    # vélos éléctriques
    ax.bar(x_pos + 0.2, df['AVG(ebike)'], color='red', alpha=0.5, label='Électrique', width=0.4, align='center')

    ax.set_ylabel('Nombre de vélos disponible en moyenne')
    ax.set_xlabel('Villes')
    ax.set_xticks(x_pos)
    if ordre == 'ASC':
        text = 'Villes (10 moins peuplées en station)'
    else:
        text = 'Villes (10 plus peuplées en station)'
    ax.set_xticklabels(df['nom_arrondissement_communes'], fontsize=5, rotation=35)
    ax.legend()
    ax.set_title('Répartition des vélos en moyenne  : ('+date_debut[:10]+' - '+date_fin[:10]+') \n'+text)
    plt.gca().xaxis.set_tick_params(labelsize=7)
    if boolean:
        plt.show()
    else:
        plt.savefig('./static/graphique/analyse_global_éléc_méca.png')
    plt.close()



def analyse_global_vélo(boolean,ordre='DESC',date_debut=(datetime.now()- timedelta(weeks=2)).strftime("%Y-%m-%d"), date_fin=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
    """boolean,String,date_début,date_fin -> None
    Préconditions : La station doit exister
    Rôle : Affiche le nombre de vélos disponibles à la station en fonction du temps en forme de graphique
    Analyse le nombre de vélo dans les 10 communes les plus peuplées ou moins peuplées en station
    Postconditions : Affiche le graphique"""

    df = SQL.select_table(mycursor, 'station_status', 'AVG(numbikesavailable),nom_arrondissement_communes', "WHERE is_installed = 1 AND date_insertion BETWEEN date('" + date_debut + "') AND date('" + date_fin + "') GROUP BY nom_arrondissement_communes ORDER BY COUNT(DISTINCT stationcode) "+ordre+" LIMIT 10 ;")

    # Extraire les données de la DataFrame
    moyennes = df['AVG(numbikesavailable)']
    arrondissements = df['nom_arrondissement_communes']

    # Tracer l'histogramme
    plt.bar(arrondissements, moyennes)
    plt.ylabel('Nombre moyen de vélos disponibles')
    if ordre== 'ASC':
        text='Villes (10 moins peuplées en station)'
    else:
        text='Villes (10 plus peuplées en station)'
    plt.title('Nombre moyen de vélos disponibles ('+date_debut[:10]+' - '+date_fin[:10]+') \n' + text)
    plt.xticks( fontsize=6,rotation=35)
    plt.tight_layout()
    if boolean:
        plt.show()
    else:
        plt.savefig('./static/graphique/analyse_global_vélo.png')
    plt.close()



def analyse_par_département_actif_inactif(boolean):
    """boolean -> void
    Rôle : Affiche un graphique montrant le nombre de station actif et inactif inactif. Par département Parisien
    Postconditions : Affiche le graphique"""
    # Récupérer les données
    df = SQL.select_table(mycursor, "station_status", "stationcode,is_installed,numdocksavailable,numbikesavailable,mechanical,ebike,nom_arrondissement_communes,MAX(date_insertion)", "WHERE stationcode < 21000 Group by stationcode")
    df = df.assign(departement=df['stationcode'].apply(lambda x: str(x.split('_')[0])[:-3] if str(x)[:-3] else None))

    fig, ax = plt.subplots()
    # graphique des stations actifs ou non
    ax.bar(df['departement'].unique(), df.groupby('departement')['is_installed'].sum(), color='blue', alpha=0.5, label='Actif')
    ax.bar(df['departement'].unique(), df.groupby('departement')['is_installed'].count() - df.groupby('departement')['is_installed'].sum(), bottom=df.groupby('departement')['is_installed'].sum(), color='red', alpha=0.5, label='Inactif')
    ax.set_ylabel('Nombre de stations')
    ax.set_xlabel('Départements')
    ax.legend()
    ax.set_title('Répartition des stations actives et inactives par département\n'+time.strftime("%Y-%m-%d %H:%M", time.localtime()))
    if boolean:
        plt.show()
    else:
        plt.savefig('./static/graphique/analyse_par_département_actif_inactif.png')
    plt.close()

def nombre_vélo_ville(boolean,commune="Paris",date_debut=(datetime.now()- timedelta(weeks=2)).strftime("%Y-%m-%d"), date_fin=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
    """boolean,String,date_début,date_fin -> None
    Rôle : Affiche le nombre de vélos disponibles des stations en fonction du temps en forme de graphique
    Dans une commune donnée et en forme de graphique à point"""
    # Récupérer les données
    df = SQL.select_table(mycursor, "station_status", "nom_arrondissement_communes,AVG(numbikesavailable),date_insertion", "WHERE is_installed = 1 AND date_insertion BETWEEN date('" + date_debut + "') AND date('" + date_fin + "') AND nom_arrondissement_communes LIKE '"+commune+"' Group by DATE_FORMAT(date_insertion, '%Y-%m-%d %H')")
    # Extraire les données de la DataFrame
    dates = df['date_insertion']
    moyennes = df['AVG(numbikesavailable)']
    # Tracer le graphique
    plt.plot(dates, moyennes, '-*')
    plt.xlabel('Date d\'insertion')
    plt.ylabel('Moyenne des vélos disponibles')
    plt.title('Nombre de vélos disponibles sur '+commune+'('+date_debut[:10]+' - '+date_fin[:10]+')')
    plt.grid(which='major', axis='x', color='black', linestyle='dashed')
    plt.grid(which='major', axis='y', color='black', linestyle='dashed')
    plt.xticks(rotation=45)
    plt.tight_layout()
    if boolean:
        plt.show()
    else:
        plt.savefig('./static/graphique/nombre_vélo_ville_'+commune+'.png')
    plt.close()

def nombre_vélo_ville_éléc_méca(boolean,commune="Paris",date_debut=(datetime.now()- timedelta(weeks=2)).strftime("%Y-%m-%d"), date_fin=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
    """boolean,String,date_début,date_fin -> None
    Rôle : Affiche le nombre de vélos disponibles des stations en fonction du temps en forme de graphique
    Dans une commune donnée et en forme de graphique à point"""
    # Récupérer les données
    df = SQL.select_table(mycursor, "station_status", "nom_arrondissement_communes,AVG(mechanical),AVG(ebike),date_insertion", "WHERE is_installed = 1 AND date_insertion BETWEEN date('" + date_debut + "') AND date('" + date_fin + "') AND nom_arrondissement_communes LIKE '"+commune+"' Group by DATE_FORMAT(date_insertion, '%Y-%m-%d %H')")
    # Extraire les données de la DataFrame
    dates = df['date_insertion']
    mechanical = df['AVG(mechanical)']
    ebike = df['AVG(ebike)']
    # Tracer le graphique
    plt.plot(dates, mechanical, '-*')
    plt.plot(dates, ebike, '-*')
    plt.xlabel('Date d\'insertion')
    plt.ylabel('Moyenne des vélos disponibles')
    plt.title('Nombre de vélos disponibles sur '+commune+'('+date_debut[:10]+' - '+date_fin[:10]+')')
    plt.legend(['vélo mécanique','vélo électrique'])
    plt.grid(which='major', axis='x', color='black', linestyle='dashed')
    plt.grid(which='major', axis='y', color='black', linestyle='dashed')
    plt.xticks(rotation=45)
    plt.tight_layout()
    if boolean:
        plt.show()
    else:
        plt.savefig('./static/graphique/nombre_vélo_ville_éléc_méca'+commune+'.png')
    plt.close()


def graph_global_type_vélo(boolean, limite,type='ebike', date_debut=(datetime.now() - timedelta(weeks=2)).strftime("%Y-%m-%d"),
                 date_fin=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())):
    """boolean,int,String,String,date_début,date_fin -> None
        Rôle : Affiche le nombre de vélos disponibles d'un type selectionner des stations en fonction du temps en forme de graphique
        Dans les n (n étant la limite indiqué) communes les plus ou moins peuplés et en forme de graphique à point"""
    myresultregion = SQL.select_table(mycursor, "station_status",
                                      "nom_arrondissement_communes,Count(DISTINCT stationcode)",
                                      "WHERE is_installed = 1 AND date_insertion BETWEEN date('" + date_debut + "') AND date('" + date_fin + "') GROUP BY nom_arrondissement_communes ORDER BY COUNT(DISTINCT stationcode) DESC LIMIT " + str(
                                          limite))
    fig, ax = plt.subplots()
    for region in myresultregion['nom_arrondissement_communes']:
        # Fait une requete pour les valeurs pour le graphique
        df = SQL.select_table(mycursor, "station_status",
                              "nom_arrondissement_communes, AVG(mechanical), AVG(ebike), date_insertion",
                              "WHERE is_installed = 1 AND date_insertion BETWEEN date('" + date_debut + "') AND date('" + date_fin + "') AND nom_arrondissement_communes LIKE '" + region + "' GROUP BY DATE_FORMAT(date_insertion, '%Y-%m-%d %H')")

        # Extraire les données de la DataFrame
        dates = df['date_insertion']
        ebike = df['AVG(' + type + ')']

        # Tracer le graphique
        ax.plot(dates, ebike, '-*')

    plt.xlabel('Date d\'insertion')
    plt.ylabel('Moyenne des vélos '+type.replace('ebike', 'éléctriques').replace('mechanical', 'mécaniques')+' disponibles')
    plt.title('Répartition des vélos '+type.replace('ebike', 'éléctriques').replace('mechanical', 'mécaniques')+' par région \n(' + date_debut[:10] + ' - ' + date_fin[:10] + ')')
    plt.legend(myresultregion['nom_arrondissement_communes'])
    plt.grid(which='major', axis='x', color='black', linestyle='dashed')
    plt.grid(which='major', axis='y', color='black', linestyle='dashed')
    plt.xticks(rotation=45)
    plt.tight_layout()
    if boolean:
        plt.show()
    else:
        plt.savefig('./static/graphique/graph_global_type_vélo_'+type+'.png')
    plt.close()

# Connexion à la base de données
mydb = mysql.connector.connect(
    host="  localhost",
    user="root",
    database="velibs"
)

# Création du curseur
mycursor = mydb.cursor()

if __name__ == "__main__":
    """Fait un exemple si le fichier est main
    Affiche les graphiques et ne les enregistre pas"""
    graph_global_type_vélo(True, 5,'ebike','2023-04-10', '2023-06-04')
    graph_global_type_vélo(True, 5, 'mechanical', '2023-04-10', '2023-06-04')
    nombre_vélo_ville_éléc_méca(True,'Paris', '2023-04-10', '2023-06-04')
    analyse_global_éléc_méca(True,'ASC')
    analyse_global_éléc_méca(True)
    analyse_global_vélo(True,'ASC')
    analyse_global_vélo(True)
    nombre_vélo_ville(True)
    analyse_par_region_vélo_élec_méca(5, True)
    analyse_par_station_dock_available(12109, True)
    analyse_par_département_actif_inactif(True)

    analyse_par_station_éléc_méca(12109,True)
