from app import app
from models.models import db, Categorie, Actualite, Concert, Utilisateur, Commentaire
from datetime import datetime, timedelta

with app.app_context():
    print("Nettoyage de la base de données...")
    db.drop_all() 
    db.create_all()

    print("Création Administrateur et Utilisateurs de test...")
    admin = Utilisateur(login="admin", password="password123", est_admin=True)
    visiteur = Utilisateur(login="visiteur", password="password123", est_admin=False)
    u_rock = Utilisateur(login="rock_fan99", password="password123", est_admin=False)
    u_jazz = Utilisateur(login="miles_davis_fan", password="password123", est_admin=False)
    u_electro = Utilisateur(login="daft_punker", password="password123", est_admin=False)
    
    db.session.add_all([admin, visiteur, u_rock, u_jazz, u_electro])
    db.session.commit()

    print("Création des catégories et actualités...")
    c_electro = Categorie(nom="Electro")
    c_rock = Categorie(nom="Rock")
    c_jazz = Categorie(nom="Jazz")
    db.session.add_all([c_electro, c_rock, c_jazz])
    db.session.commit()

    a1 = Actualite(titre="Justice annonce une nouvelle tournée mondiale", contenu="Le duo français iconique est de retour avec un show lumière qui promet de révolutionner le genre.", categorie_id=c_electro.id)
    a2 = Actualite(titre="Le renouveau du Post-Punk en France", contenu="De nombreux groupes émergent sur la scène indépendante parisienne, ramenant les guitares saturées sur le devant de la scène.", categorie_id=c_rock.id)
    a3 = Actualite(titre="Festival Django Reinhardt : Programmation", contenu="Le célèbre festival dévoile une affiche exceptionnelle pour son édition estivale avec Ibrahim Maalouf en tête d'affiche.", categorie_id=c_jazz.id)
    db.session.add_all([a1, a2, a3])

    print("Création des concerts à venir...")
    date_proche = datetime.now() + timedelta(days=5) 
    date_lointaine = datetime.now() + timedelta(days=45) 
    
    co_futur1 = Concert(artiste="Tomorrowland Winter", lieu="Alpe d'Huez", date_concert=date_proche, places_max=20000, places_occupees=19500, est_passe=False, description="Le plus grand festival électro à la montagne. Préparez vos doudounes !")
    co_futur2 = Concert(artiste="Hellfest 2024", lieu="Clisson", date_concert=date_lointaine, places_max=60000, places_occupees=59990, est_passe=False, description="L'édition la plus brutale du festival mythique de musiques extrêmes.")
    
    db.session.add_all([co_futur1, co_futur2])

    print("Création des concerts passés...")
    co_passe_rock = Concert(
        artiste="Arctic Monkeys", lieu="Accor Arena, Paris", date_concert=datetime(2023, 5, 10), 
        places_max=20000, places_occupees=20000, est_passe=True, 
        avis_redacteur="Un show d'une classe absolue. Alex Turner a hypnotisé la salle de bout en bout.",
        image_url="https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?auto=format&fit=crop&w=800&q=80"
    )
    
    co_passe_jazz = Concert(
        artiste="Ibrahim Maalouf", lieu="Olympia, Paris", date_concert=datetime(2023, 12, 1), 
        places_max=2000, places_occupees=2000, est_passe=True, 
        avis_redacteur="Une fusion parfaite entre jazz oriental et musique urbaine. Le public était en transe.",
        image_url="https://images.unsplash.com/photo-1511192336575-5a79af67a629?auto=format&fit=crop&w=800&q=80"
    )

    co_passe_electro = Concert(
        artiste="Daft Punk Tribute", lieu="Rex Club, Paris", date_concert=datetime(2024, 2, 15), 
        places_max=800, places_occupees=800, est_passe=True, 
        avis_redacteur="Un hommage vibrant qui a fait trembler les murs du Rex jusqu'au petit matin.",
        image_url="https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=800&q=80"
    )
    
    db.session.add_all([co_passe_rock, co_passe_jazz, co_passe_electro])
    db.session.commit()

    print("Ajout des commentaires de test...")
    
    # Avis sur le concert Rock
    db.session.add(Commentaire(contenu="Incroyable ! Ils ont joué '505' à la fin, j'en ai pleuré !", concert_id=co_passe_rock.id, utilisateur_id=u_rock.id, date_post=datetime(2023, 5, 11, 8, 30)))
    db.session.add(Commentaire(contenu="L'acoustique de la salle n'était pas folle sur les premiers morceaux, mais le groupe a tout cassé.", concert_id=co_passe_rock.id, utilisateur_id=visiteur.id, date_post=datetime(2023, 5, 12, 14, 15)))
    
    # Avis sur le concert Jazz
    db.session.add(Commentaire(contenu="Un génie. Tout simplement. La trompette à quarts de ton me donnera toujours des frissons.", concert_id=co_passe_jazz.id, utilisateur_id=u_jazz.id, date_post=datetime(2023, 12, 2, 9, 0)))
    db.session.add(Commentaire(contenu="Première fois que je voyais du Jazz en live, je ne regrette absolument pas, l'ambiance était survoltée.", concert_id=co_passe_jazz.id, utilisateur_id=u_rock.id, date_post=datetime(2023, 12, 5, 18, 45)))
    db.session.add(Commentaire(contenu="Magique. On attend la prochaine tournée avec impatience.", concert_id=co_passe_jazz.id, utilisateur_id=visiteur.id, date_post=datetime(2023, 12, 10, 20, 0)))

    # Avis sur le concert Electro
    db.session.add(Commentaire(contenu="Même si ce ne sont pas les vrais, fermer les yeux et entendre Rollin' & Scratchin' avec ce système son... wow.", concert_id=co_passe_electro.id, utilisateur_id=u_electro.id, date_post=datetime(2024, 2, 16, 11, 20)))

    db.session.commit()

    print("--- Base de données prête ! ---")
    print("Comptes disponibles pour tester :")
    print("Admin    -> login: admin       | pass: password123")
    print("Visiteur -> login: visiteur     | pass: password123")
    print("Autres   -> login: rock_fan99  | pass: password123")