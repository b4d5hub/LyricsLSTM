from flask import Flask, render_template, request, jsonify
import numpy as np
import pickle
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)

# Charger le modèle et le tokenizer
print("Chargement du modèle...")
model = load_model('taylor_swift_lstm.keras')
with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

SEQ_LENGTH = 20
print("✅ Modèle chargé !")

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    seed      = data.get('seed', 'shake it off')
    words     = int(data.get('words', 25))
    temp      = float(data.get('temperature', 0.8))

    lyrics = generate_lyrics(seed, next_words=words, temperature=temp)
    return jsonify({'lyrics': lyrics, 'seed': seed})

if __name__ == '__main__':
    app.run(debug=True)