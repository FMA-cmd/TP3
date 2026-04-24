# app.py
from flask import Flask
from models.database import db

app = Flask(__name__)
app.secret_key = 'super_cle_secrete_musiactu'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/musiactu_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Liaison de SQLAlchemy à l'application Flask
db.init_app(app)

@app.route('/')
def accueil():
    return "<h1>Bienvenue sur MusiActu !</h1><p>Configuration de la BDD terminée.</p>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)