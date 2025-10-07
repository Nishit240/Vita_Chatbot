import tkinter as tk
import tkinter.font as tkFont
from datetime import datetime
import json
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import pyjokes
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
# -----------------------------
# 1) Load training data from JSON
# -----------------------------
with open(r"C:\Main\Education\PYTHON\project\Vita_ML_ChatBot\training_data.json", encoding="utf-8") as f:
    training_data = json.load(f)


X_train = list(training_data.keys())
y_train = list(training_data.values())

model = make_pipeline(TfidfVectorizer(ngram_range=(1,2)), MultinomialNB())
model.fit(X_train, y_train)

# -----------------------------
# 2) Keyword fallback
# -----------------------------
intent_responses = {
    "greeting": ["hey", "good morning", "good evening"],
    "goodbye": ["bye", "exit", "quit", "see you"],
    "thanks": ["thank you", "thanks", "thx"],
    "joke": ["joke", "funny", "laugh"],
    # "please": ["please", "can you", "would you", "plx", "pls"],
    # "affirmative": ["yes", "yeah", "yup", "sure", "ok", "okay"],
    # "negative": ["no", "nah", "nope", "not really"]
     
}
def show_joke():
    joke_1 = pyjokes.get_joke(language="en", category="neutral")
    return joke_1

fallback_answers = {
    "greeting": "Hello! How can I help you today?",
    "goodbye": "Goodbye! Have a nice day! 👋",
    "thanks": "You're welcome! 😊",
    "joke": show_joke,
    # "please": "Please, I'd be happy to help!",
    # "affirmative": "Great! How can I assist you further? 🙂💡",
    # "negative": "Alright, no problem! Let me know if you need anything else. 🙂✌️"
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

    # Calculator
    try:
        if any(op in user_input_clean for op in ["+", "-", "*", "/", "**", "%"]):
            return f"The answer is {eval(user_input_clean)}"
    except:
        return "Sorry, I couldn't calculate that. Please try a valid math expression."

    # Check JSON-based responses
    for key in training_data:
        if key in user_input_clean:
            return training_data[key]
        
    # Keyword fallback
    cleaned = clean_text(user_input)
    for intent, keywords in intent_responses.items():
        for word in keywords:
            if word in cleaned:
                # Special case for jokes → call function every time
                if intent == "joke":
                    return show_joke() + " 😄"
                else:
                    return fallback_answers[intent]


    # ML-based prediction
    try:
        return model.predict([user_input])[0]
    except:
        return "Sorry, I don't understand that.\nType 'Help' to see what I can answer."
    
# -----------------------------
# 4) GUI 
# -----------------------------
def add_message(sender, message, align="left", color="#FFFFFF"):
    time_now = datetime.now().strftime("%H:%M")
    outer_frame = tk.Frame(chat_frame, bg="#F0F0F0")
    outer_frame.pack(fill="x", pady=2, anchor="w" if align == "left" else "e")

    top_row = tk.Frame(outer_frame, bg="#F0F0F0")
    if sender == "You":
        tk.Label(top_row, text="👦🏻", font=("Arial", 20), bg="#F0F0F0").pack(side="right")
        tk.Label(top_row, text=time_now, font=("Arial", 8), bg="#F0F0F0", fg="black").pack(side="right", padx=(0, 2))
    else:
        tk.Label(top_row, text="🤖", font=("Arial", 20), bg="#F0F0F0").pack(side="left")
        tk.Label(top_row, text=time_now, font=("Arial", 8), bg="#F0F0F0", fg="black").pack(side="left", padx=(1, 0))
    top_row.pack(fill="x")

    font = tkFont.Font(family="Arial", size=12) 
    max_width_px = 350
    chars_per_line = max_width_px // font.measure("a")
    line_count = message.count("\n") + 1
    lines = max(line_count, (len(message) // chars_per_line) + 1)
    width = min(len(message), chars_per_line)

    msg_text = tk.Text(
        outer_frame, bg=color, fg="black", wrap="word", font=("Arial", 12),
        relief="flat", padx=10, pady=5, height=lines, width=width
    )
    msg_text.insert("1.0", message)
    msg_text.configure(state="disabled")  
    msg_text.pack(anchor="w" if align == "left" else "e", padx=15, pady=2)

    chat_canvas.update_idletasks()
    chat_canvas.yview_moveto(1.0)

# -----------------------------
# 5) Send Message
# -----------------------------
def send_message():
    user_input = user_entry.get()
    if user_input.strip():
        add_message("You", user_input, align="right", color="#96A78D")
        response = get_response(user_input)
        add_message("Vita", response, align="left", color="#D9E9CF")
        user_entry.delete(0, tk.END)
    if user_input.lower() in ["quit", "bye"]:
        root.destroy()

# -----------------------------
# 6) GUI Setup
# -----------------------------
root = tk.Tk()
root.title("Vita ChatBot")
root.geometry("440x650")
root.config(bg="#96A78D")

title_label = tk.Label(root, text="⌬ Vita Chatbot", font=("Helvetica", 20, "bold"),
                       fg="#F0F0F0", bg="#96A78D", pady=10)
title_label.pack(fill=tk.X)

chat_area_frame = tk.Frame(root, bg="#F0F0F0")  
chat_area_frame.pack(fill="both", expand=True, padx=10, pady=(10, 0))

chat_canvas = tk.Canvas(chat_area_frame, bg="#F0F0F0", highlightthickness=0)
scrollbar = tk.Scrollbar(chat_area_frame, orient="vertical", command=chat_canvas.yview)

chat_frame = tk.Frame(chat_canvas, bg="#F0F0F0")
chat_frame.bind("<Configure>", lambda e: chat_canvas.configure(scrollregion=chat_canvas.bbox("all")))

chat_window = chat_canvas.create_window((0, 0), window=chat_frame, anchor="nw")

def resize_chat_frame(event):
    chat_canvas.itemconfig(chat_window, width=event.width)

chat_canvas.bind("<Configure>", resize_chat_frame)
chat_canvas.configure(yscrollcommand=scrollbar.set)

chat_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

bottom_frame = tk.Frame(root, bg="#96A78D")
bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)

user_entry = tk.Entry(bottom_frame, font=("Arial", 14), relief="solid", bd=1, bg="#96A78D", fg="#F0F0F0")
user_entry.insert(0, "Help")
user_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
user_entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(
    bottom_frame, text="⌯⌲", bg="#96A78D", fg="#F0F0F0", font=("Arial", 15, "bold"),
    width=3, command=send_message
)
send_button.pack(side="right")

add_message("Vita", "Hello! I'm Vita, your assistant.", align="left", color="#D9E9CF")
add_message("Vita", "Type 'Help' to see what I can do.", align="left", color="#D9E9CF")


root.mainloop()
