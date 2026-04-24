from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

class CommentaireForm(FlaskForm):
    """Formulaire pour poster un avis [cite: 11, 26]"""
    pseudo = StringField('Nom', validators=[DataRequired(), Length(min=2, max=50)])
    message = TextAreaField('Mon commentaire', validators=[DataRequired()])
    submit = SubmitField('Envoyer')

class ReservationForm(FlaskForm):
    """Formulaire simple de réservation [cite: 16]"""
    nb_places = IntegerField('Nombre de places', validators=[DataRequired()])
    submit = SubmitField('Réserver')