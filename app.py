from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

# Importation de la base de données et des modèles (MVC) [cite: 23]
from models.models import db, Concert, Actualite, Categorie, Utilisateur
# Importation des formulaires Flask-WTF 
from forms.forms import LoginForm, ActualiteForm

app = Flask(__name__, template_folder='views')
app.secret_key = 'super_cle_secrete_musiactu'

# --- CONFIGURATION DE LA BASE DE DONNÉES (MariaDB) [cite: 24] ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://tp_user:tp_pass@localhost/musiactu_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation des extensions
db.init_app(app)

# Gestion de la connexion (Flask-Login) 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redirige ici si accès interdit

@login_manager.user_loader
def load_user(user_id):
    """Charge l'utilisateur pour la session Flask-Login."""
    return Utilisateur.query.get(int(user_id))

# ==========================================
#              ROUTES PUBLIQUES
# ==========================================

@app.route('/')
def accueil():
    """Page d'accueil : affiche les 3 dernières actualités et concerts[cite: 20]."""
    actus = Actualite.query.order_by(Actualite.date_pub.desc()).limit(3).all()
    concerts = Concert.query.filter(Concert.est_passe == False).limit(3).all()
    return render_template('index.html', actus=actus, concerts=concerts)

@app.route('/concerts')
def concerts():
    """Liste tous les concerts à venir[cite: 15]."""
    liste_concerts = Concert.query.all()
    return render_template('concerts.html', concerts=liste_concerts)

@app.route('/actualites')
def actualites():
    """Affiche toutes les actualités[cite: 19]."""
    liste_actus = Actualite.query.order_by(Actualite.date_pub.desc()).all()
    return render_template('actualites.html', actus=liste_actus, titre_page="Toute l'Actualité Musicale")

@app.route('/actualites/<genre>')
def actualites_par_genre(genre):
    """Affiche les actualités filtrées par genre (Jazz, Rock, Electro)[cite: 19]."""
    categorie = Categorie.query.filter(Categorie.nom.ilike(genre)).first_or_404()
    actus_filtrees = Actualite.query.filter_by(categorie_id=categorie.id).all()
    return render_template('actualites.html', actus=actus_filtrees, titre_page=f"Actualités {categorie.nom}")

# ==========================================
#           ESPACE ADMINISTRATION 
# ==========================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Gère l'authentification des administrateurs."""
    form = LoginForm()
    if form.validate_on_submit():
        user = Utilisateur.query.filter_by(login=form.login.data).first()
        # Note : Dans un vrai projet, utilisez check_password_hash
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
    """Déconnecte l'utilisateur."""
    logout_user()
    return redirect(url_for('accueil'))

@app.route('/admin/ajouter-actu', methods=['GET', 'POST'])
@login_required
def ajouter_actu():
    """Formulaire d'ajout d'une actualité (réservé aux admins)."""
    form = ActualiteForm()
    # On remplit le menu déroulant avec les catégories de la BDD
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)