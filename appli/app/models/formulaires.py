from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, IntegerField


class InsertionPersonne(FlaskForm):
    idWikidata =  StringField("id_illustre", validators=[]) 
    nomIllustre =  StringField("nom_illustre", validators=[])
    ddn =  StringField("ddn", validators=[])
    ddm =  StringField("ddm", validators=[])
    genre =  SelectField("genre", choices=[], validators=[])
    image =  StringField("image", validators=[])
    article =  StringField("article", validators=[])

class InsertionMaison(FlaskForm):
    id =  StringField("id", validators=[]) 
    denomination =  StringField("denomination", validators=[])
    code_postal =  StringField("code_postal", validators=[])
    adresse =  StringField("adresse", validators=[])
    commune =  StringField("commune", validators=[])
    dpmt =  StringField("dpmt", validators=[])
    region =  SelectField("region", choices=[], validators=[])
    code_INSEE =  StringField("code_INSEE", validators=[])
    pays =  StringField("pays", validators=[])
    date_label =  StringField("date_label", validators=[])
    latitude =  StringField("latitude", validators=[])
    longitude =  StringField("longitude", validators=[])
    museeFrance =  BooleanField("musee_france", validators=[])
    monumentsInscrits =  BooleanField("monuments_inscrits", validators=[])
    monumentsClasses =  BooleanField("monuments_classes", validators=[])
    nombreSPR =  IntegerField("nombre_SPR", validators=[])
    type =  SelectField("type", choices=[], validators = [])
    idWikidata =  SelectField("id_wikidata", choices = [], validators=[])

class UpdateMaisons(FlaskForm):
    id =  StringField("id", validators=[]) 
    denomination =  StringField("denomination", validators=[])
    code_postal =  StringField("code_postal", validators=[])
    adresse =  StringField("adresse", validators=[])
    commune =  StringField("commune", validators=[])
    dpmt =  StringField("dpmt", validators=[])
    region =  SelectField("region", choices=[], validators=[])
    code_INSEE =  StringField("code_INSEE", validators=[])
    pays =  StringField("pays", validators=[])
    date_label =  StringField("date_label", validators=[])
    latitude =  StringField("latitude", validators=[])
    longitude =  StringField("longitude", validators=[])
    museeFrance =  BooleanField("musee_france", validators=[])
    monumentsInscrits =  BooleanField("monuments_inscrits", validators=[])
    monumentsClasses =  BooleanField("monuments_classes", validators=[])
    nombreSPR =  IntegerField("nombre_SPR", validators=[])
    type =  SelectField("type", choices=[], validators = [])
    idWikidata =  SelectField("id_wikidata", choices = [], validators=[])


class Recherche(FlaskForm):
    type =  SelectField("type", choices=[], validators = [])
    region = SelectField("region", choices=[], validators=[])
    genre = SelectField("genre", choices=[], validators=[])
    periode = SelectField("periode", choix=[], validators=[])
    museeFrance =  BooleanField("musee_france", validators=[])
    monumentsInscrits =  BooleanField("monuments_inscrits", validators=[])
    monumentsClasses =  BooleanField("monuments_classes", validators=[])

