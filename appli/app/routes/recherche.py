from ..app import app, db
from flask import render_template, request
from sqlalchemy import or_
from ..models.formulaires import Recherche
from ..models.data import Maisons, Personnes, Domaine, Genre
from ..utils.transformations import nettoyage_string_to_int, clean_arg



@app.route("/recherche", methods=['GET', 'POST'])
@app.route("/recherche/<int:page>", methods=['GET', 'POST'])
def recherche(page=1):
    form = Recherche()
    personnes_instance = Personnes()
    distinct_periode = personnes_instance.get_distinct_siecles()
    distinct_regions = Maisons.get_distinct_regions()
    form.region.choices = [('','')] + [(region, region) for region in distinct_regions]
    form.type.choices = [('','')] + [(domaine.value, domaine.value) for domaine in Domaine]
    form.genre.choices = [('','')] + [(genre.value, genre.value) for genre in Genre]
    form.periode.choices = [('','')] + [(periode.value, periode.value) for periode in distinct_periode]

    # initialisation des données de retour dans le cas où il n'y ait pas de requête
    donnees = []

    if form.validate_on_submit():
        # récupération des éventuels arguments de l'URL qui seraient le signe de l'envoi d'un formulaire
        denomination = clean_arg(request.form.get("region", None))
        region =  clean_arg(request.form.get("region", None))
        type =  clean_arg(request.form.get("type", None))
        genre =  clean_arg(request.form.getlist("genre", None))
        periode = clean_arg(request.form.getlist("periode", None))
        museeFrance =  clean_arg(request.form.get("musee_france", None))
        monumentsInscrits =  clean_arg(request.form.get("monuments_inscrits", None))
        monumentsClasses =  clean_arg(request.form.get("monuments_classes", None))

        # si l'un des champs de recherche a une valeur, alors cela veut dire que le formulaire a été rempli et qu'il faut lancer une recherche 
        # dans les données
        if denomination or region  or type or genre or museeFrance or monumentsClasses or monumentsInscrits or periode :
            # initialisation de la recherche; en fonction de la présence ou nom d'un filtre côté utilisateur, nous effectuerons des filtres SQLAlchemy,
            # ce qui signifie que nous pouvons jouer ici plusieurs filtres d'affilée
            query_results = Maisons.query

            if denomination:
                query_results = query_results.filter(Maisons.denomination.ilike("%"+denomination.lower()+"%")) #.lower ou pas ?

            if region : 
                query_results = query_results.filter(Maisons.region == region)

            if type : 
                query_results = query_results.filter(Maisons.type == type)

            if museeFrance:
                query_results = query_results.filter(Maisons.museeFrance == True)
            
            if monumentsInscrits:
                query_results = query_results.filter(Maisons.monumentsInscrits == True)

            if monumentsClasses:
                query_results = query_results.filter(Maisons.monumentsClasses == True)
            
            if genre :
                genre = db.session.execute("""select a.id from maisons a 
                    inner join personnes b on b.idWikidata = a.idWikiata and b.resource  == '"""+genre+"""'
                    """).fetchall()
                query_results = query_results.filter(Maisons.id.in_([g.id for g in genre] ))
            
            if periode:
                periode = db.session.execute("""select a.id from maisons a 
                    inner join personnes b on b.idWikidata = a.idWikidata and siecles_vie == '"""+periode+"""'
                    """).fetchall()
                query_results = query_results.filter(Maisons.id.in_([p.id for p in periode] ))
            
            donnees = query_results.order_by(Maisons.name).paginate(page=page, per_page=app.config["PAYS_PER_PAGE"])

            # renvoi des filtres de recherche pour préremplissage du formulaire
            form.denomination.data = denomination
            form.region.data = region
            form.type.data = type

    return render_template("pages/liste2.html", 
            sous_titre= "Recherche", 
            donnees=donnees,
            form=form)


'''
@app.route("/recherche_rapide")
@app.route("/recherche_rapide/<int:page>")
def recherche_rapide(page=1):
    chaine =  request.args.get("chaine", None)

    if chaine:
        resources = db.session.execute("""select a.id from country a 
            inner join country_resources b on b.id = a.id 
            inner join resources c on c.name = b.resource and (c.name like '%"""+chaine+"""%' or  c.id like '%"""+chaine+"""%')
            """).fetchall()
        
        maps = db.session.execute("""select a.id from country a 
            inner join country_map b on b.id = a.id 
            inner join map  c on c.name = b.map_ref and (c.name like '%"""+chaine+"""%' or  c.id like '%"""+chaine+"""%')
            """).fetchall()

        resultats = Country.query.\
            filter(
                or_(
                    Country.name.ilike("%"+chaine+"%"),
                    Country.type.ilike("%"+chaine+"%"),
                    Country.Introduction.ilike("%"+chaine+"%"),
                    Country.id.in_([r.id for r in resources] + [m.id for m in maps])
                )
            ).\
            distinct(Country.name).\
            order_by(Country.name).\
            paginate(page=page, per_page=app.config["PAYS_PER_PAGE"])
    else:
        resultats = None
        
    return render_template("pages/resultats_recherche_pays.html", 
            sous_titre= "Recherche | " + chaine, 
            donnees=resultats,
            requete=chaine)

'''