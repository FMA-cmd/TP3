from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

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