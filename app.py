from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'ma_cle_secrete_123'
db = SQLAlchemy(app)

# --- CONFIGURATION DE LA CONNEXION ---
login_manager = LoginManager(app)
login_manager.login_view = 'login' # Si on n'est pas connecté, le site nous renvoie ici

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- MODÈLES (Base de données) ---
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), default='resident')

# NOUVEAU : La table pour enregistrer les plats
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)

# --- ROUTES ---

@app.route('/')
def home():
    # Par défaut, on envoie les gens vers la page d'inscription pour l'instant
    return redirect(url_for('inscription'))

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form.get('username')
        mdp = request.form.get('password')
        role = request.form.get('role')
        
        # Vérifier si l'utilisateur existe déjà
        user_exists = User.query.filter_by(username=nom).first()
        if user_exists:
            return "Cet utilisateur existe déjà !"

        nouvel_utilisateur = User(username=nom, password=mdp, role=role)
        db.session.add(nouvel_utilisateur)
        db.session.commit()
        
        # Une fois inscrit, on l'envoie vers la page de connexion
        return redirect(url_for('login'))
    
    return render_template('inscription.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nom = request.form.get('username')
        mdp = request.form.get('password')
        
        # On cherche l'utilisateur dans la base
        user = User.query.filter_by(username=nom).first()
        
        # On vérifie si l'utilisateur existe ET si le mot de passe correspond
        if user and user.password == mdp:
            login_user(user) # Flask-Login crée la session
            return redirect(url_for('dashboard'))
        else:
            return "Erreur : Mauvais nom d'utilisateur ou mot de passe."

    return render_template('login.html')

@app.route('/dashboard')
@login_required # Cette ligne protège la page : impossible d'y aller sans être connecté
def dashboard():
    # Page d'accueil temporaire pour voir si la connexion marche
    return f"""
    <h1>Bienvenue {current_user.username} !</h1>
    <p>Ton rôle est : <strong>{current_user.role}</strong></p>
    <br>
    <a href='/logout'>Se déconnecter</a>
    """

@app.route('/logout')
@login_required
def logout():
    logout_user() # Ferme la session
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Va créer la nouvelle table Recipe automatiquement
    app.run(debug=True)