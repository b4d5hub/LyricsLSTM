from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import os
import pymysql
import numpy as np
import pickle
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'taylor_secret_key_13'

# Configuration MySQL will be overridden by Environment variables in Serverless deployment
def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('MYSQL_HOST', '127.0.0.1'),
        port=int(os.environ.get('MYSQL_PORT', 3307)),
        user=os.environ.get('MYSQL_USER', 'root'),
        password=os.environ.get('MYSQL_PASSWORD', ''),
        database=os.environ.get('MYSQL_DB', 'taylor_db')
    )

# Charger le modèle LSTM
print("Chargement du modèle LSTM...")
model = load_model('taylor_swift_lstm.keras')
with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

SEQ_LENGTH = 20
print("✅ Système prêt !")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Veuillez vous connecter pour accéder à cette page.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def generate_lyrics(seed_text, next_words=30, temperature=0.8):
    result = seed_text
    current_seed = seed_text.lower()

    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([current_seed])[0]
        token_list = pad_sequences(
            [token_list],
            maxlen=SEQ_LENGTH - 1,
            padding='pre'
        )

        predictions = model.predict(token_list, verbose=0)[0]
        predictions = np.log(predictions + 1e-10) / temperature
        predictions = np.exp(predictions) / np.sum(np.exp(predictions))

        predicted_index = np.random.choice(len(predictions), p=predictions)
        output_word = tokenizer.index_word.get(predicted_index, "")

        current_seed += " " + output_word
        result += " " + output_word

    return result

# --- PUBLIC ROUTES ---

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('generator'))
    return render_template('home.html')

@app.route('/technology')
def technology():
    return render_template('technology.html')

@app.route('/process')
def process():
    return render_template('process.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users(username, email, password) VALUES(%s, %s, %s)", 
                        (username, email, hashed_pw))
            conn.commit()
            flash("Compte créé avec succès ! Connectez-vous.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            print("DB Insert Error:", e)
            flash("Erreur lors de l'inscription.", "error")
        finally:
            cur.close()
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, username, password FROM users WHERE email = %s", [email])
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('generator'))
        else:
            flash("Email ou mot de passe incorrect.", "error")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Déconnexion réussie.", "success")
    return redirect(url_for('home'))

# --- PROTECTED ROUTES ---

@app.route('/generator')
@login_required
def generator():
    return render_template('index.html', username=session.get('username'))

@app.route('/generate', methods=['POST'])
@login_required
def generate():
    data = request.get_json()
    seed      = data.get('seed', 'shake it off')
    words     = int(data.get('words', 25))
    temp      = float(data.get('temperature', 0.8))

    lyrics = generate_lyrics(seed, next_words=words, temperature=temp)
    return jsonify({'lyrics': lyrics, 'seed': seed})

if __name__ == '__main__':
    app.run(debug=True)