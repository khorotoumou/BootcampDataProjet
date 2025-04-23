from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Exemple de base de connaissances
responses = {
    "livraison": "Votre commande est généralement livrée sous 3 à 5 jours ouvrés.",
    "retour": "Vous pouvez retourner un produit sous 14 jours après réception.",
    "compte": "Cliquez sur 'Mot de passe oublié' pour le réinitialiser.",
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json['message'].lower()
    # Détection basique d’intent (à améliorer avec NLP)
    if "livraison" in user_msg:
        intent = "livraison"
    elif "retour" in user_msg:
        intent = "retour"
    elif "compte" in user_msg or "mot de passe" in user_msg:
        intent = "compte"
    else:
        intent = None

    response = responses.get(intent, "Je n'ai pas compris votre demande. Souhaitez-vous parler à un conseiller ?")
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
