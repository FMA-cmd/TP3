from flask import Flask, render_template

app = Flask(__name__, template_folder='views')
app.secret_key = 'super_cle_secrete_musiactu'

@app.route('/')
def accueil():
    return render_template('index.html')


@app.route('/concerts')
def concerts():
    liste_concerts = [
        {"titre": "Musilac 2024", "date": "01/07/2024", "lieu": "Aix-les-Bains", "type": "Festival"},
        {"titre": "Jazz à Vienne", "date": "15/07/2024", "lieu": "Vienne", "type": "Jazz"}
    ]
    return render_template('concerts.html', concerts=liste_concerts)

@app.route('/actualites')
def actualites():
    liste_actus = [
        {"titre": "Le nouvel album de Daft Punk ?", "categorie": "Electro", "date": "Il y a 2 jours"},
        {"titre": "Retour du Rock en 2024", "categorie": "Rock", "date": "Il y a 1 semaine"}
    ]
    return render_template('actualites.html', actus=liste_actus)

@app.route('/actualites/<genre>')
def actualites_par_genre(genre):
    toutes_les_actus = [
        {"titre": "Le nouvel album de Daft Punk ?", "categorie": "Electro", "date": "Il y a 2 jours"},
        {"titre": "Retour du Rock en 2024", "categorie": "Rock", "date": "Il y a 1 semaine"},
        {"titre": "Miles Davis à l'honneur", "categorie": "Jazz", "date": "Hier"}
    ]
    actus_filtrees = [actu for actu in toutes_les_actus if actu['categorie'].lower() == genre.lower()]
    return render_template('actualites.html', actus=actus_filtrees, titre_page=f"Actualités {genre.capitalize()}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)