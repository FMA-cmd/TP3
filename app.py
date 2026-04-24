from flask import Flask, render_template

# On précise à Flask que les fichiers HTML se trouvent dans le dossier 'views'
app = Flask(__name__, template_folder='views')
app.secret_key = 'super_cle_secrete_musiactu'

# Route pour la page d'accueil
@app.route('/')
def accueil():
    # render_template va chercher le fichier index.html dans le dossier views
    # Pour l'instant, on envoie des listes vides, on connectera la BDD juste après
    return render_template('index.html', actus=[], concerts=[])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)