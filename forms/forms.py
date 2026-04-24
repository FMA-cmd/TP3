from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms import IntegerField

class CommentaireForm(FlaskForm):
    """Formulaire pour poster un avis"""
    pseudo = StringField('Nom', validators=[DataRequired(), Length(min=2, max=50)])
    message = TextAreaField('Mon commentaire', validators=[DataRequired()])
    submit = SubmitField('Envoyer')

class ReservationForm(FlaskForm):
    """Formulaire simple de réservation"""
    nb_places = IntegerField('Nombre de places', validators=[DataRequired()])
    submit = SubmitField('Réserver')



class LoginForm(FlaskForm):
    login = StringField("Nom d'utilisateur", validators=[DataRequired()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Se connecter")

class ActualiteForm(FlaskForm):
    titre = StringField("Titre de l'article", validators=[DataRequired()])
    contenu = TextAreaField("Contenu", validators=[DataRequired()])
    # On remplira les choix de la catégorie dynamiquement dans la route
    categorie_id = SelectField("Catégorie", coerce=int)
    submit = SubmitField("Publier l'actualité")

class InscriptionForm(FlaskForm):
    """Formulaire pour les nouveaux visiteurs"""
    login = StringField("Nom d'utilisateur", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField("Confirmez le mot de passe", validators=[DataRequired(), EqualTo('password', message='Les mots de passe doivent correspondre.')])
    submit = SubmitField("Créer mon compte")

class ReservationForm(FlaskForm):
    """Formulaire pour réserver des places"""
    nb_places = IntegerField("Nombre de places", validators=[DataRequired()], default=1)
    submit = SubmitField("Confirmer la réservation")