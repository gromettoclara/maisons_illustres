from ..app import app, db
from flask import render_template, request
from sqlalchemy import or_
from ..models.data import Maisons, Personnes, Domaine, Genre
from ..models.formulaires import Recherche
from ..utils.parse import convertir_geojson


@app.route("/", methods=['GET', 'POST'])
@app.route("/accueil", methods=['GET', 'POST'])
def maisons():
    """
    Gère la route "/accueil" qui s'ouvre aussi au démarrage de l'application.

    Returns
    -------
    render_template
        Un modèle HTML pour la une page d'informations générales.
    """

    return render_template("pages/accueil.html", 
        sous_titre="Accueil")


@app.route("/maisons/<string:nom_maisons>")
def info_maisons(nom_maisons):
    """
    Gère la route "/maisons/<nom_maisons>" pour afficher les informations sur une maison spécifique.

    Parameters
    ----------
    nom_maisons : str
        Le nom de la maison dont les informations doivent être affichées.

    Returns
    -------
    render_template
        Un modèle HTML pour la page d'informations sur la maison avec les données.
    """
    # Récupère les données de la maison en fonction du nom fourni.
    donnees= Maisons.query.filter(Maisons.denomination == nom_maisons).first()
    # Récupère les informations sur la personne associée à la maison.
    personne = Personnes.query.filter(Personnes.idWikidata == str(donnees.idWikidata)).first()

    return render_template("pages/info_maisons.html", 
        sous_titre=nom_maisons, 
        donnees=donnees,
        personne=personne)


@app.route("/personnes", methods=['GET', 'POST'])
@app.route("/personnes/<int:page>", methods=['GET', 'POST'])
def personnes(page=1):
    """
    Gère la route "/personnes" pour afficher une liste paginée des illustres. 
    Des boutons dans le templates HTML permettront d'en modifier les informations ou de les supprimer. 
    Cette solution a été trouvée pour décoreller la suppression des maisons de celle des personnes, car une personne peut posséder plusieurs maisons. 

    Parameters
    ----------
    page : int, optional
        Numéro de la page à afficher, par défaut 1.

    Returns
    -------
    render_template
        Un modèle HTML pour la page de la liste des personnes avec les données paginées à afficher.
    """
    
    # Récupère les données paginées des personnes ordonnées par nomIllustre.
    donnees = Personnes.query.order_by(Personnes.nomIllustre).paginate(page=page, per_page=app.config["MAISONS_PER_PAGE"])

    return render_template("pages/liste_personnes.html", 
        sous_titre="Liste des personnes", 
        donnees=donnees)




@app.route("/carte", methods=['GET'])
def carte():
    """
    Gère la route "/carte" pour afficher une carte des maisons.

    Returns
    -------
    render_template
        Un modèle HTML pour la page "/carte" avec les données à afficher.
    """
    # Récupère toutes les maisons de la base de données. 
    maisons = Maisons.query.all()
    # Initialisation de la liste des dico de données pertinentes sur les maisons. 
    donnees = []

    # Pour chaque maison, récupère la personne et les informations associées. 
    for maison in maisons:
        personne = Personnes.query.filter(Personnes.idWikidata == maison.idWikidata).first()
        donnees.append(
            {
                'lat': maison.latitude,
                'lon': maison.longitude,
                'popup': maison.make_popup(),
                'domaine': maison.type.value if maison.type else None, 
                'museeFrance':maison.museeFrance, 
                'monClasse' : maison.monumentsClasses,
                'monInscrit' : maison.monumentsInscrits,
                'genre': personne.genre.value if personne and maison.type else None,
                'ddn_pers' : personne.ddn if personne else 0
            }
        )
    
    # Convertit les données en GeoJSON.
    donnees = convertir_geojson(donnees)
    
    return render_template("pages/carte.html",
        sous_titre="Carte",
        donnees = donnees)

 
@app.route("/graphiques", methods=['GET', 'POST'])
def graphiques():
    """
    Gère la route "/graphiques" pour afficher deux datavisualisations permettant l'exploitation des données de notre base.

    Returns
    -------
    render_template : 
        Un modèle HTML pour la page "/graphiques" ainsi que les données nécessaires à la construction et visualisation des graphiques :
        
        - labels_genres : Liste des catégories de genre des personnes illustres.
        - counts_genres : Nombre d'illustres pour chaque catégorie de genre.
        - labels_types : Liste des domaines intellectuels auxquels se rattachent les différentes maisons.
        - counts_types : Nombre de maisons rattachées à chaque domaine intellectuel.
        - sous_titre : Titre à afficher dans l'onglet de la page.
    """
    # Récupérer les données pour le premier graphique (genres des personnes illustres)
    genres_count = db.session.query(Personnes.genre, db.func.count(Personnes.nomIllustre)).group_by(Personnes.genre).all()
    labels_genres = [result[0].value if result[0] is not None else 'NULL' for result in genres_count]
    counts_genres = [result[1] for result in genres_count]

    # Récupérer les données pour le deuxième graphique (domaines des maisons)
    types_count = db.session.query(Maisons.type, db.func.count(Maisons.id)).group_by(Maisons.type).all()
    labels_types = [result[0].value if result[0] is not None else 'Non renseigné' for result in types_count]
    counts_types = [result[1] for result in types_count]

    # Rendre le template avec les données nécessaires pour les graphiques
    return render_template('pages/graphiques.html', 
                           labels_genres=labels_genres, counts_genres=counts_genres,
                           labels_types=labels_types, counts_types=counts_types, 
                           sous_titre = "Graphiques")
