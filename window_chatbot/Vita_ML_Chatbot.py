import json
import string
import pyjokes
import warnings
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

warnings.filterwarnings("ignore", category=UserWarning)

# -----------------------------
# 1) Load training data (robust path)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAINING_DATA_FILE = os.path.join(BASE_DIR, "training_data.json")

with open(TRAINING_DATA_FILE, encoding="utf-8") as f:
    training_data = json.load(f)

X_train = list(training_data.keys())
y_train = list(training_data.values())

model = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), MultinomialNB())
model.fit(X_train, y_train)

# -----------------------------
# 2) Keyword fallback
# -----------------------------
intent_responses = {
    "greeting": ["hey", "good morning", "good evening"],
    "goodbye": ["bye", "exit", "quit", "see you"],
    "thanks": ["thank you", "thanks", "thx"],
    "joke": ["joke", "funny", "laugh"],
}

def show_joke():
    return pyjokes.get_joke(language="en", category="neutral")

fallback_answers = {
    "greeting": "Hello! How can I help you today?",
    "goodbye": "Goodbye! Have a nice day! 👋",
    "thanks": "You're welcome! 😊",
    "joke": show_joke,
}

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

# -----------------------------
# 3) Get Response
# -----------------------------
def get_response(user_input):
    user_input_clean = user_input.lower()

    # Calculator support
    try:
        if any(op in user_input_clean for op in ["+", "-", "*", "/", "**", "%"]):
            return f"The answer is {eval(user_input_clean)}"
    except:
        return "Sorry, I couldn't calculate that. Please try a valid math expression."

    # JSON-based responses
    for key in training_data:
        if key in user_input_clean:
            return training_data[key]

    # Keyword fallback
    cleaned = clean_text(user_input)
    for intent, keywords in intent_responses.items():
        for word in keywords:
            if word in cleaned:
                if intent == "joke":
                    return show_joke() + " 😄"
                else:
                    return fallback_answers[intent]

    # ML-based prediction
    try:
        return model.predict([user_input])[0]
    except:
        return "Sorry, I don't understand that.\nType 'Help' to see what I can answer."
