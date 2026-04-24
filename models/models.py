from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin


db = SQLAlchemy()

class Categorie(db.Model):
    """Représente les genres musicaux (Jazz, Rock, Electro) [cite: 19]"""
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    actualites = db.relationship('Actualite', backref='categorie', lazy=True)

class Actualite(db.Model):
    """Stocke les articles d'actualité [cite: 13, 19]"""
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    date_pub = db.Column(db.DateTime, default=datetime.utcnow)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'))

class Concert(db.Model):
    """Gère les événements et les réservations [cite: 15, 16]"""
    id = db.Column(db.Integer, primary_key=True)
    artiste = db.Column(db.String(100), nullable=False)
    lieu = db.Column(db.String(100), nullable=False)
    date_concert = db.Column(db.DateTime, nullable=False)
    places_max = db.Column(db.Integer, nullable=False)
    places_occupees = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    est_passe = db.Column(db.Boolean, default=False)

class Commentaire(db.Model):
    """Commentaires pour les concerts passés """
    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_post = db.Column(db.DateTime, default=datetime.utcnow)
    concert_id = db.Column(db.Integer, db.ForeignKey('concert.id'))

class Utilisateur(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    est_admin = db.Column(db.Boolean, default=False)