from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import requests
from datetime import datetime, timedelta

from models.models import db, Concert, Actualite, Categorie, Utilisateur, Commentaire
from forms.forms import LoginForm, ActualiteForm, InscriptionForm, ReservationForm, CommentaireForm, CategorieForm, ConcertForm

app = Flask(__name__, template_folder='views')
app.secret_key = 'super_cle_secrete_musiactu'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://tp_user:tp_pass@localhost/musiactu_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))

def obtenir_meteo(ville, date_concert):
    aujourd_hui = datetime.now()
    ecart = (date_concert - aujourd_hui).days
    if 0 <= ecart <= 15:
        try:
            url_geo = f"https://geocoding-api.open-meteo.com/v1/search?name={ville}&count=1&language=fr"
            reponse_geo = requests.get(url_geo).json()
            if not reponse_geo.get("results"): return None
                
            lat = reponse_geo["results"][0]["latitude"]
            lon = reponse_geo["results"][0]["longitude"]

            url_meteo = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,precipitation_sum&timezone=auto"
            reponse_meteo = requests.get(url_meteo).json()

            date_str = date_concert.strftime('%Y-%m-%d')
            if date_str in reponse_meteo["daily"]["time"]:
                index = reponse_meteo["daily"]["time"].index(date_str)
                temp = reponse_meteo["daily"]["temperature_2m_max"][index]
                pluie = reponse_meteo["daily"]["precipitation_sum"][index]
                etat = "Pluvieux 🌧️" if pluie > 2 else "Ensoleillé / Nuageux ⛅"
                return f"{temp}°C - {etat}"
        except Exception:
            return None
    return None

# === ROUTES PUBLIQUES ===
@app.route('/')
def accueil():
    actus = Actualite.query.order_by(Actualite.date_pub.desc()).limit(3).all()
    concerts = Concert.query.filter(Concert.est_passe == False).limit(3).all()
    return render_template('index.html', actus=actus, concerts=concerts)

@app.route('/concerts')
def concerts():
    liste_concerts = Concert.query.order_by(Concert.date_concert.desc()).all()
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
            flash('Compte créé avec succès ! Connectez-vous.', 'success')
            return redirect(url_for('login'))
    return render_template('inscription.html', form=form)

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

@app.route('/concert/<int:id>', methods=['GET', 'POST'])
def detail_concert(id):
    concert = Concert.query.get_or_404(id)
    form_resa = ReservationForm()
    form_comm = CommentaireForm()
    
    places_restantes = concert.places_max - concert.places_occupees
    meteo = obtenir_meteo(concert.lieu, concert.date_concert)

    # SOUMISSION RESERVATION
    if 'nb_places' in request.form:
        if form_resa.validate_on_submit():
            if not current_user.is_authenticated:
                flash('Vous devez être connecté pour réserver.', 'warning')
                return redirect(url_for('login'))
            nb_demandees = form_resa.nb_places.data
            if 0 < nb_demandees <= places_restantes:
                concert.places_occupees += nb_demandees
                db.session.commit()
                flash(f'Réservation de {nb_demandees} place(s) validée !', 'success')
                return redirect(url_for('concerts'))
            else:
                flash('Nombre de places insuffisant.', 'danger')

    # SOUMISSION COMMENTAIRE
    if 'contenu' in request.form:
        if form_comm.validate_on_submit():
            if not current_user.is_authenticated:
                flash('Vous devez être connecté pour commenter.', 'warning')
                return redirect(url_for('login'))
            
            nouveau_comm = Commentaire(contenu=form_comm.contenu.data, concert_id=concert.id, utilisateur_id=current_user.id)
            db.session.add(nouveau_comm)
            db.session.commit()
            flash('Commentaire publié avec succès !', 'success')
            return redirect(url_for('detail_concert', id=concert.id))
        else:
            flash('Votre commentaire doit faire au moins 5 caractères.', 'danger')

    return render_template('concert_detail.html', concert=concert, form_resa=form_resa, form_comm=form_comm, places_restantes=places_restantes, meteo=meteo)

# === ADMINISTRATION ===
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.est_admin: return redirect(url_for('accueil'))
    return render_template('admin_dashboard.html', actus=Actualite.query.all(), concerts=Concert.query.all(), categories=Categorie.query.all())

@app.route('/admin/ajouter-actu', methods=['GET', 'POST'])
@login_required
def ajouter_actu():
    if not current_user.est_admin: return redirect(url_for('accueil'))
    form = ActualiteForm()
    form.categorie_id.choices = [(c.id, c.nom) for c in Categorie.query.all()]
    if form.validate_on_submit():
        nouvelle = Actualite(titre=form.titre.data, contenu=form.contenu.data, categorie_id=form.categorie_id.data)
        db.session.add(nouvelle)
        db.session.commit()
        flash('Actualité publiée !', 'success')
        return redirect(url_for('actualites'))
    return render_template('ajouter_actu.html', form=form)

@app.route('/admin/modifier-actu/<int:id>', methods=['GET', 'POST'])
@login_required
def modifier_actu(id):
    if not current_user.est_admin: return redirect(url_for('accueil'))
    actu = Actualite.query.get_or_404(id)
    form = ActualiteForm(obj=actu)
    form.categorie_id.choices = [(c.id, c.nom) for c in Categorie.query.all()]
    if form.validate_on_submit():
        form.populate_obj(actu)
        db.session.commit()
        flash("Actualité modifiée !", "success")
        return redirect(url_for('admin_dashboard'))
    return render_template('modifier_generique.html', form=form, titre=f"Modifier : {actu.titre}")

@app.route('/admin/modifier-concert/<int:id>', methods=['GET', 'POST'])
@login_required
def modifier_concert(id):
    if not current_user.est_admin: return redirect(url_for('accueil'))
    concert = Concert.query.get_or_404(id)
    form = ConcertForm(obj=concert)
    if form.validate_on_submit():
        form.populate_obj(concert)
        db.session.commit()
        flash("Concert mis à jour !", "success")
        return redirect(url_for('admin_dashboard'))
    return render_template('modifier_generique.html', form=form, titre=f"Modifier : {concert.artiste}")

@app.route('/admin/modifier-categorie/<int:id>', methods=['GET', 'POST'])
@login_required
def modifier_categorie(id):
    if not current_user.est_admin: return redirect(url_for('accueil'))
    cat = Categorie.query.get_or_404(id)
    form = CategorieForm(obj=cat)
    if form.validate_on_submit():
        cat.nom = form.nom.data
        db.session.commit()
        flash("Catégorie renommée !", "success")
        return redirect(url_for('admin_dashboard'))
    return render_template('modifier_generique.html', form=form, titre=f"Modifier catégorie : {cat.nom}")

@app.route('/admin/supprimer/<type_item>/<int:id>')
@login_required
def supprimer_item(type_item, id):
    if not current_user.est_admin: return redirect(url_for('accueil'))
    if type_item == 'actu':
        item = Actualite.query.get_or_404(id)
    elif type_item == 'concert':
        item = Concert.query.get_or_404(id)
    elif type_item == 'categorie':
        item = Categorie.query.get_or_404(id)
    else:
        return redirect(url_for('admin_dashboard'))
    db.session.delete(item)
    db.session.commit()
    flash(f"Élément supprimé avec succès !", "success")
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)