from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    login = StringField("Nom d'utilisateur", validators=[DataRequired()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Se connecter")

class InscriptionForm(FlaskForm):
    """Formulaire pour les nouveaux visiteurs"""
    login = StringField("Nom d'utilisateur", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField("Confirmez le mot de passe", validators=[DataRequired(), EqualTo('password', message='Les mots de passe doivent correspondre.')])
    submit = SubmitField("Créer mon compte")

class ActualiteForm(FlaskForm):
    titre = StringField("Titre de l'article", validators=[DataRequired()])
    contenu = TextAreaField("Contenu", validators=[DataRequired()])
    categorie_id = SelectField("Catégorie", coerce=int)
    submit = SubmitField("Publier l'actualité")

class ReservationForm(FlaskForm):
    """Formulaire pour réserver des places"""
    nb_places = IntegerField("Nombre de places", validators=[DataRequired()], default=1)
    submit = SubmitField("Confirmer la réservation")

class CommentaireForm(FlaskForm):
    """Formulaire pour laisser un avis sur un concert passé"""
    contenu = TextAreaField("Votre avis sur le concert", validators=[DataRequired(), Length(min=5)])
    submit = SubmitField("Publier mon commentaire")