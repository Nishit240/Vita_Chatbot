from flask import Flask, render_template, request, jsonify
from Vita_ML_Chatbot import get_response

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    bot_response = get_response(user_input)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="127.0.0.2", port=5500, debug=True)
