from flask import Flask, render_template
from models.models import db, Concert, Actualite, Categorie

app = Flask(__name__, template_folder='views')
app.secret_key = 'super_cle_secrete_musiactu'

# --- CONFIGURATION DE LA BASE DE DONNÉES ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://tp_user:tp_pass@localhost/musiactu_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# C'est cette ligne qui relie SQLAlchemy à ton application Flask !
db.init_app(app)

@app.route('/')
def accueil():
    return render_template('index.html')


@app.route('/concerts')
def concerts():
    # On récupère TOUS les concerts dans la BDD
    liste_concerts = Concert.query.all()
    return render_template('concerts.html', concerts=liste_concerts)

@app.route('/actualites')
def actualites():
    # On récupère toutes les actus triées par date de publication (de la plus récente à la plus ancienne)
    liste_actus = Actualite.query.order_by(Actualite.date_pub.desc()).all()
    return render_template('actualites.html', actus=liste_actus, titre_page="Toute l'Actualité Musicale")

@app.route('/actualites/<genre>')
def actualites_par_genre(genre):
    # 1. On cherche la catégorie correspondante dans la BDD (insensible à la casse)
    categorie = Categorie.query.filter(Categorie.nom.ilike(genre)).first_or_404()
    
    # 2. On récupère les actus liées à l'ID de cette catégorie
    actus_filtrees = Actualite.query.filter_by(categorie_id=categorie.id).all()
    
    return render_template('actualites.html', actus=actus_filtrees, titre_page=f"Actualités {categorie.nom}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)