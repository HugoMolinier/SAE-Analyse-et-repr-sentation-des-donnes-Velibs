from flask import Flask, render_template,request,Response
import creation_carte
import Analyse
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SESSION_REFRESH_EACH_REQUEST'] = True # Permet d'effectuer des requêtes de façon simultanées

@app.route('/')
def index():
    """Fonction qui permet d'afficher la page d'accueil du site et de créer la carte de Paris"""
    creation_carte.creation_carte_paris()
    return render_template('index.html', image_path='./static/image_site/blanc.jpg',image_path2='./static/image_site/blanc.jpg')


@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    """Fonction qui permet de récupérer les données du formulaire et d'afficher les graphiques correspondants"""
    creation_carte.creation_carte_paris()
    function_type = request.form.get('function_type')
    value_min_date = request.form.get('value_min_date')
    value_max_date = request.form.get('value_max_date')
    input_station = request.form.get('input_station')
    region= request.form.get('region')
    ordre = request.form.get('ordre')
    #Si aucune date n'est renseignée, on prend les 2 dernières semaines
    if value_min_date=="":
        value_min_date=(datetime.now()- timedelta(weeks=2)).strftime("%Y-%m-%d")
    if value_max_date=="":
        value_max_date=datetime.now().strftime("%Y-%m-%d")
    try:
        # On affiche les graphiques correspondants à la fonction choisie
        if function_type == 'function1':
            Analyse.analyse_par_station_éléc_méca(input_station,False,value_min_date,value_max_date)
            Analyse.analyse_par_station_dock_available(input_station,False,value_min_date,value_max_date)
            return render_template('index.html', image_path='./static/graphique/analyse_par_station_éléc_méca.png',image_path2='./static/graphique/analyse_par_station_dock_available.png')
        elif function_type == 'function2':
            Analyse.analyse_par_region_vélo_élec_méca(5, False,value_min_date,value_max_date)
            Analyse.nombre_vélo_ville_éléc_méca(False,region,value_min_date,value_max_date)
            return render_template('index.html', image_path='./static/graphique/analyse_par_region_'+region+'.png',image_path2='./static/graphique/nombre_vélo_ville_éléc_méca'+region+'.png')
        elif function_type == 'function3':
            Analyse.analyse_global_éléc_méca(False,ordre,value_min_date,value_max_date)
            return render_template('index.html', image_path='./static/graphique/analyse_global_éléc_méca.png',image_path2='./static/image_site/blanc.jpg')
        elif function_type=='function4':
            Analyse.analyse_par_département_actif_inactif(False)
            return render_template('index.html', image_path='./static/graphique/analyse_par_département_actif_inactif.png',image_path2='./static/image_site/blanc.jpg')
        elif function_type == 'function5':
            Analyse.graph_global_type_vélo(False,5,'ebike',value_min_date,value_max_date)
            Analyse.graph_global_type_vélo(False,5,'mechanical',value_min_date,value_max_date)
            return render_template('index.html', image_path='./static/graphique/graph_global_type_vélo_ebike.png',image_path2='./static/graphique/graph_global_type_vélo_mechanical.png')
        elif function_type == 'function6':
            Analyse.analyse_global_vélo(False,ordre,value_min_date,value_max_date)
            return render_template('index.html', image_path='./static/graphique/analyse_global_vélo.png',image_path2='./static/image_site/blanc.jpg')
        elif function_type == 'function7':
            Analyse.nombre_vélo_ville(False,region,value_min_date,value_max_date)
            return render_template('index.html', image_path='./static/graphique/nombre_vélo_ville_'+region+'.png',image_path2='./static/image_site/blanc.jpg')

    except:
        print('Erreur')
        return render_template('index.html', image_path='./static/image_site/blanc.jpg',image_path2='./static/image_site/blanc.jpg')

    return render_template('index.html', image_path='./static/image_site/blanc.jpg',image_path2='./static/image_site/blanc.jpg')


if __name__ == '__main__':
    app.run() 