# init_db.py
from app import app
from models.models import db, Categorie, Actualite, Concert, Utilisateur 
from datetime import datetime

with app.app_context():
    print("--- Démarrage de l'initialisation de la base de données ---")
    
    # 1. On supprime tout pour éviter les erreurs de colonnes manquantes
    print("Suppression des anciennes tables...")
    db.drop_all() 
    
    # 2. On recrée les tables avec la nouvelle structure (incluant 'est_admin')
    print("Création des nouvelles tables...")
    db.create_all()

    # 3. Création du compte Administrateur (est_admin=True)
    print("Création du compte Administrateur...")
    admin = Utilisateur(login="admin", password="password123", est_admin=True)
    db.session.add(admin)
    
    # 4. Création d'un compte Visiteur de test (est_admin=False)
    print("Création d'un compte Visiteur de test...")
    visiteur = Utilisateur(login="testuser", password="user123", est_admin=False)
    visiteur2 = Utilisateur(login="faouzi", password="salut", est_admin=False)
    db.session.add(visiteur)
    db.session.add(visiteur2)

    # 5. Création des catégories
    print("Injection des catégories...")
    c_electro = Categorie(nom="Electro")
    c_rock = Categorie(nom="Rock")
    c_jazz = Categorie(nom="Jazz")
    db.session.add_all([c_electro, c_rock, c_jazz])
    db.session.commit() # On commit pour récupérer les IDs des catégories

    # 6. Création des actualités (News)
    print("Injection des actualités...")
    a1 = Actualite(
        titre="Le nouvel album de Daft Punk ?", 
        contenu="Des rumeurs persistantes annoncent un retour du duo casqué en studio pour 2024...", 
        categorie_id=c_electro.id
    )
    a2 = Actualite(
        titre="Retour du Rock en 2024", 
        contenu="Les guitares saturent à nouveau les ondes avec l'émergence d'une nouvelle scène rock garage.", 
        categorie_id=c_rock.id
    )
    a3 = Actualite(
        titre="Jazz à Vienne : Programmation dévoilée", 
        contenu="Le festival mythique revient avec une tête d'affiche internationale qui va ravir les puristes.", 
        categorie_id=c_jazz.id
    )
    db.session.add_all([a1, a2, a3])

    # 7. Création des concerts
    print("Injection des concerts...")
    co1 = Concert(
        artiste="Musilac", 
        lieu="Aix-les-Bains", 
        # On met une date très proche pour déclencher l'API Météo !
        date_concert=datetime(2026, 4, 28), 
        places_max=10000,
        places_occupees=0,
        description="Le plus grand festival pop-rock de la région sur les bords du lac du Bourget.",
        est_passe=False # On s'assure qu'il n'est pas passé
    )
    co2 = Concert(
        artiste="Jazz à Vienne", 
        lieu="Vienne", 
        date_concert=datetime(2024, 7, 15), 
        places_max=5000,
        places_occupees=4950, # Presque complet pour tester les limites
        description="Une soirée magique dans le théâtre antique de Vienne."
    )
    db.session.add_all([co1, co2])

    db.session.commit()
    print("\n--- Base de données initialisée avec succès ! ---")
    print("Identifiants Admin : admin / password123")
    print("Identifiants User  : testuser / user123")
    print("Identifiants User  : faouzi / salut")