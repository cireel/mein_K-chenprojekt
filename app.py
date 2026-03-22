from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# --- ROUTES ---

@app.route('/')
def home():
    # Page de connexion
    return "<h1>Bienvenue ! Ici se trouvera la page de connexion.</h1>"

@app.route('/dashboard')
def dashboard():
    # Page où les résidents voient le menu et votent
    return "<h1>Tableau de bord des résidents</h1>"

@app.route('/proposer', methods=['GET', 'POST'])
def proposer():
    if request.method == 'POST':
        # Ici on récupérera les données du formulaire
        return redirect(url_for('dashboard'))
    return "<h1>Formulaire pour proposer un plat</h1>"

@app.route('/cuisine')
def cuisine():
    # Page simplifiée pour la cuisinière
    return "<h1>Interface Cuisinière - Plat du jour</h1>"

if __name__ == '__main__':
    app.run(debug=True)