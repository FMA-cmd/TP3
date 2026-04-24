from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    actualites = db.relationship('Actualite', backref='categorie', lazy=True)

class Actualite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    date_pub = db.Column(db.DateTime, default=datetime.utcnow)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'))

class Concert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artiste = db.Column(db.String(100), nullable=False)
    lieu = db.Column(db.String(100), nullable=False)
    date_concert = db.Column(db.DateTime, nullable=False)
    places_max = db.Column(db.Integer, nullable=False)
    places_occupees = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    est_passe = db.Column(db.Boolean, default=False)
    avis_redacteur = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    commentaires = db.relationship('Commentaire', backref='concert', lazy=True, cascade="all, delete-orphan")

class Utilisateur(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    est_admin = db.Column(db.Boolean, default=False)

class Commentaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.Text, nullable=False)
    date_post = db.Column(db.DateTime, default=datetime.utcnow)
    concert_id = db.Column(db.Integer, db.ForeignKey('concert.id'), nullable=False)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    auteur = db.relationship('Utilisateur', backref='commentaires')