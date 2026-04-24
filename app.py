from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import requests
from datetime import datetime, timedelta

# Importation des modèles
from models.models import db, Concert, Actualite, Categorie, Utilisateur, Commentaire
# Importation des formulaires
from forms.forms import LoginForm, ActualiteForm, InscriptionForm, ReservationForm, CommentaireForm

app = Flask(__name__, template_folder='views')
app.secret_key = 'super_cle_secrete_musiactu'

# Configuration de MariaDB
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://tp_user:tp_pass@localhost/musiactu_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Configuration de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))

def obtenir_meteo(ville, date_concert):
    """
    Fonction bonus : Récupère la météo si le concert est dans moins de 15 jours.
    Utilise l'API gratuite Open-Meteo (sans clé).
    """
    aujourd_hui = datetime.now()
    ecart = (date_concert - aujourd_hui).days

    # Si le concert est dans les 15 prochains jours
    if 0 <= ecart <= 15:
        try:
            # 1. On trouve les coordonnées GPS (Latitude/Longitude) de la ville
            url_geo = f"https://geocoding-api.open-meteo.com/v1/search?name={ville}&count=1&language=fr"
            reponse_geo = requests.get(url_geo).json()
            
            if not reponse_geo.get("results"):
                return None # Ville introuvable
                
            lat = reponse_geo["results"][0]["latitude"]
            lon = reponse_geo["results"][0]["longitude"]

            # 2. On récupère les prévisions météo pour ces coordonnées
            url_meteo = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,precipitation_sum&timezone=auto"
            reponse_meteo = requests.get(url_meteo).json()

            # 3. On extrait la température pour la date exacte du concert
            date_str = date_concert.strftime('%Y-%m-%d')
            if date_str in reponse_meteo["daily"]["time"]:
                index = reponse_meteo["daily"]["time"].index(date_str)
                temp = reponse_meteo["daily"]["temperature_2m_max"][index]
                pluie = reponse_meteo["daily"]["precipitation_sum"][index]
                
                # Formatage de la réponse
                etat = "Pluvieux 🌧️" if pluie > 2 else "Ensoleillé / Nuageux ⛅"
                return f"{temp}°C - {etat}"
        except Exception as e:
            return None # En cas d'erreur de connexion à l'API
    return None

# ==========================================
#              ROUTES PUBLIQUES
# ==========================================

@app.route('/')
def accueil():
    actus = Actualite.query.order_by(Actualite.date_pub.desc()).limit(3).all()
    concerts = Concert.query.filter(Concert.est_passe == False).limit(3).all()
    return render_template('index.html', actus=actus, concerts=concerts)

@app.route('/concerts')
def concerts():
    liste_concerts = Concert.query.all()
    return render_template('concerts.html', concerts=liste_concerts)

@app.route('/actualites')
def actualites():
    liste_actus = Actualite.query.order_by(Actualite.date_pub.desc()).all()
    return render_template('actualites.html', actus=liste_actus, titre_page="Toute l'Actualité Musicale")

@app.route('/actualites/<genre>')
def actualites_par_genre(genre):
    categorie = Categorie.query.filter(Categorie.nom.ilike(genre)).first_or_404()
    actus_filtrees = Actualite.query.filter_by(categorie_id=categorie.id).all()
    return render_template('actualites.html', actus=actus_filtrees, titre_page=f"Actualités {categorie.nom}")

# ==========================================
#         INSCRIPTION & RÉSERVATION & COMMENTAIRES
# ==========================================

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    form = InscriptionForm()
    if form.validate_on_submit():
        if Utilisateur.query.filter_by(login=form.login.data).first():
            flash('Ce nom d\'utilisateur est déjà pris.', 'danger')
        else:
            nouvel_user = Utilisateur(login=form.login.data, password=form.password.data, est_admin=False)
            db.session.add(nouvel_user)
            db.session.commit()
            flash('Compte créé avec succès ! Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('login'))
    return render_template('inscription.html', form=form)

@app.route('/concert/<int:id>', methods=['GET', 'POST'])
def detail_concert(id):
    concert = Concert.query.get_or_404(id)
    form_resa = ReservationForm()
    form_comm = CommentaireForm()
    
    # 1. LA LIGNE MANQUANTE ÉTAIT ICI : On calcule toujours les places restantes
    places_restantes = concert.places_max - concert.places_occupees

    # 2. Appel de la fonction météo (Bonus)
    meteo = obtenir_meteo(concert.lieu, concert.date_concert)

    # 3. CAS 1 : RÉSERVATION (Concert à venir)
    if not concert.est_passe and form_resa.validate_on_submit() and 'nb_places' in request.form:
        if not current_user.is_authenticated:
            flash('Vous devez être connecté pour réserver des places.', 'warning')
            return redirect(url_for('login'))
            
        nb_demandees = form_resa.nb_places.data
        if 0 < nb_demandees <= places_restantes:
            concert.places_occupees += nb_demandees
            db.session.commit()
            flash(f'Super ! Vous avez réservé {nb_demandees} place(s) pour {concert.artiste}.', 'success')
            return redirect(url_for('concerts'))
        else:
            flash('Nombre de places invalide ou insuffisant.', 'danger')

    # 4. CAS 2 : COMMENTAIRES (Concert passé)
    if concert.est_passe and form_comm.validate_on_submit() and 'contenu' in request.form:
        if not current_user.is_authenticated:
            flash('Vous devez être connecté pour commenter.', 'warning')
            return redirect(url_for('login'))
            
        nouveau_comm = Commentaire(
            contenu=form_comm.contenu.data,
            concert_id=concert.id,
            utilisateur_id=current_user.id
        )
        db.session.add(nouveau_comm)
        db.session.commit()
        flash('Votre commentaire a été publié avec succès !', 'success')
        return redirect(url_for('detail_concert', id=concert.id))

    # 5. On envoie tout au HTML (y compris les places_restantes !)
    return render_template('concert_detail.html', concert=concert, form_resa=form_resa, form_comm=form_comm, places_restantes=places_restantes, meteo=meteo)

# ==========================================
#           ESPACE ADMINISTRATION 
# ==========================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Utilisateur.query.filter_by(login=form.login.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('Connexion réussie !', 'success')
            return redirect(url_for('accueil'))
        else:
            flash('Identifiants incorrects.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('accueil'))

@app.route('/admin/ajouter-actu', methods=['GET', 'POST'])
@login_required
def ajouter_actu():
    if not current_user.est_admin:
        flash('Accès refusé. Réservé aux administrateurs.', 'danger')
        return redirect(url_for('accueil'))

    form = ActualiteForm()
    form.categorie_id.choices = [(c.id, c.nom) for c in Categorie.query.all()]
    
    if form.validate_on_submit():
        nouvelle = Actualite(
            titre=form.titre.data,
            contenu=form.contenu.data,
            categorie_id=form.categorie_id.data
        )
        db.session.add(nouvelle)
        db.session.commit()
        flash('Actualité publiée avec succès !', 'success')
        return redirect(url_for('actualites'))
    
    return render_template('ajouter_actu.html', form=form)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Affiche le tableau de bord avec toutes les données."""
    if not current_user.est_admin:
        flash("Accès refusé.", "danger")
        return redirect(url_for('accueil'))
    
    # On récupère toutes les données de la base
    actus = Actualite.query.all()
    concerts = Concert.query.order_by(Concert.date_concert.desc()).all()
    categories = Categorie.query.all()
    
    return render_template('admin_dashboard.html', actus=actus, concerts=concerts, categories=categories)

@app.route('/admin/supprimer/<type_item>/<int:id>')
@login_required
def supprimer_item(type_item, id):
    """Route générique pour supprimer un élément (Actu, Concert ou Catégorie)."""
    if not current_user.est_admin:
        return redirect(url_for('accueil'))
        
    if type_item == 'actu':
        item = Actualite.query.get_or_404(id)
    elif type_item == 'concert':
        item = Concert.query.get_or_404(id)
        # Sécurité : on supprime d'abord les commentaires liés au concert
        Commentaire.query.filter_by(concert_id=id).delete() 
    elif type_item == 'categorie':
        item = Categorie.query.get_or_404(id)
        # Sécurité : on supprime les actus liées à cette catégorie
        Actualite.query.filter_by(categorie_id=id).delete() 
    else:
        return redirect(url_for('admin_dashboard'))
    
    db.session.delete(item)
    db.session.commit()
    flash(f"Élément supprimé avec succès !", "success")
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)