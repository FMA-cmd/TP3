# init_db.py
from app import app
from models.models import db, Categorie, Actualite, Concert
from datetime import datetime

with app.app_context():
    # Crée la base de données et toutes les tables basées sur models.py
    db.create_all()

    # Si la table Categorie est vide, on ajoute des données de test
    if not Categorie.query.first():
        print("Injection des données de test...")
        
        # 1. Création des catégories
        c_electro = Categorie(nom="Electro")
        c_rock = Categorie(nom="Rock")
        c_jazz = Categorie(nom="Jazz")
        db.session.add_all([c_electro, c_rock, c_jazz])
        db.session.commit() # On sauvegarde pour générer les IDs

        # 2. Création des actualités
        a1 = Actualite(titre="Le nouvel album de Daft Punk ?", contenu="Des rumeurs...", categorie_id=c_electro.id)
        a2 = Actualite(titre="Retour du Rock en 2024", contenu="Le rock n'est pas mort !", categorie_id=c_rock.id)
        db.session.add_all([a1, a2])

        # 3. Création des concerts
        co1 = Concert(artiste="Musilac 2024", lieu="Aix-les-Bains", date_concert=datetime(2024, 7, 1), places_max=10000)
        co2 = Concert(artiste="Jazz à Vienne", lieu="Vienne", date_concert=datetime(2024, 7, 15), places_max=5000)
        db.session.add_all([co1, co2])

        db.session.commit()
        print("Base de données initialisée avec succès !")
    else:
        print("Les données existent déjà.")