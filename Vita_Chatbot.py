import tkinter as tk
import tkinter.font as tkFont
from datetime import datetime

# ------------------------
# Response Logic
# ------------------------
def get_response(user_input):
    user_input = user_input.lower()

    try:
        if any(op in user_input for op in ["+", "-", "*", "/", "**", "%"]):
            return f"The answer is {eval(user_input)}"
    except:
        return "Sorry, I couldn't calculate that. Please try a valid math expression."

    responses = {
            "hello": "Hello! How can I assist you today? 👋",
    "hi": "Hi there! How are you doing? 😊",
    "how are you": "I'm doing great! Thanks for asking. How about you? 🤖",
    "your name": "I'm Vita, your personal chatbot assistant. 🤗",
    "who created you": "I was created by Nishit using Python and Machine Learning. 🧑‍💻",
    "thank you": "You're welcome! Glad I could help. 😄✨",
    "bye": "Goodbye! Wishing you a wonderful day ahead! 👋🌟",
    "age": "I don't have an age like humans — I exist digitally forever! 😉💻",
    "tell me a joke": "Why did the computer go to the doctor? Because it caught a virus! 😂💉",
    "what services do you provide": "We provide website development, mobile apps, and AI-powered solutions. 🌐🤖📱",
    "office location": "Our head office is located in Indore, India, but we serve clients globally. 🏢🌏",
    "contact information": "You can reach us via email at abcd@abc.com 📧 or call us on +91 9234567890 📞",
    "email address": "Sure! You can email us at abcd@abc.com 📧",
    "phone number": "You can call us anytime at +91 9234567890 📞",
    
    "help": "Here are the things you can ask me:\n- Hello / Hi / Vita 👋\n- How Are You 🤖\n- What Is Your Name 📝\n- Who Created You 🧑‍💻\n- Thank You / Bye / Quit ✨\n- Age / Joke 😄\n- You Can Also Use A Calculator 🧮\n\n- Company FAQs:\n- What Services Do You Offer 🌐\n- Where Are You Located 🏢\n- How Can I Contact You 📧📞\n- What Are Your Working Hours ⏰\n- Do You Offer Support 🛠️\n- What Technologies Do You Use 💻\n- How Much Does A Project Cost 💰\n- How Experienced Is Your Team 🏆\n- Do You Provide Custom Solutions 🛠️",
    
    "good morning": "Good morning! Hope your day is full of energy and success! ☀️🌸",
    "good night": "Good night! Sweet dreams and take care. 🌙💤",
    "what is artificial intelligence": "Artificial Intelligence (AI) is a branch of computer science that focuses on creating machines that can think and act intelligently. 🤖💡",
    "tell me a story": "Sure! Once upon a time, in a digital world of algorithms, a little chatbot wanted to help humans... 📖✨",
    "customer support": "You can reach our support team at support@abc.com 📧 or call +91 9876543210 📞",
    "favorite color": "I like all colors, but if I had to choose — I'd go with electric blue! 💙⚡",
    "favorite superhero": "I really like Iron Man, because he uses technology just like me! 🦾🦸‍♂️",
    "vita": "Yes, I'm here. How can I assist you? 🤗",
    "ok": "Alright! Do you need any further assistance? 👍",
    "business hours": "We are open from Monday to Friday, 10 AM to 7 PM IST. ⏰",
    "tech support": "Yes, we provide 24/7 technical support through chat, email, and phone calls. 🛠️📞",
    "technologies used": "Our team works with PHP, JavaScript, React, Node.js, HTML, CSS, and other modern technologies. 💻🌐",
    "project pricing": "Project pricing depends on your requirements. Please share your details to get a customized quote. 💰📝",
    "team experience": "Our team has over 9 years of professional experience in software development and consulting. 🏆💼",
    "custom solutions": "Yes, we design and develop tailored solutions to meet each client's specific needs. 🛠️✨",
    "yes": "Great! How can I assist you further? 😄👍",
    "no": "Alright, no problem! Let me know if you need anything else. 😌✌️",
    "okay": "Okay! Let me know if you have more questions. 🙂💡"
    }

    
    for key in responses:
        if key in user_input:
            return responses[key]

    return "Sorry, I don't understand that. Type 'Help' to see what I can answer."


# ------------------------
# Add Chat Bubble
# ------------------------
def add_message(sender, message, align="left", color="#FFFFFF"):
    time_now = datetime.now().strftime("%H:%M")

    outer_frame = tk.Frame(chat_frame, bg="white")
    outer_frame.pack(fill="x", pady=2, anchor="w" if align == "left" else "e")

    top_row = tk.Frame(outer_frame, bg="white")
    if sender == "You":
        tk.Label(top_row, text="👦🏻", font=("Arial", 20), bg="white").pack(side="right")
        tk.Label(top_row, text=time_now, font=("Arial", 8), bg="white", fg="black").pack(side="right", padx=(0, 2))
    else:
        tk.Label(top_row, text="🤖", font=("Arial", 20), bg="white").pack(side="left")
        tk.Label(top_row, text=time_now, font=("Arial", 8), bg="white", fg="black").pack(side="left", padx=(1, 0))
    top_row.pack(fill="x")

    font = tkFont.Font(family="Arial", size=12) 
    max_width_px = 350
    chars_per_line = max_width_px // font.measure("a")
    line_count = message.count("\n") + 1
    lines = max(line_count, (len(message) // chars_per_line) + 1)
    width = min(len(message), chars_per_line)

    msg_text = tk.Text(
        outer_frame, bg=color, fg="white", wrap="word", font=("Arial", 12),
        relief="flat", padx=10, pady=5, height=lines, width=width
    )
    msg_text.insert("1.0", message)
    msg_text.configure(state="disabled")  
    msg_text.pack(anchor="w" if align == "left" else "e", padx=15, pady=2)

    chat_canvas.update_idletasks()
    chat_canvas.yview_moveto(1.0)


# ------------------------
# Send Message
# ------------------------
def send_message():
    user_input = user_entry.get()
    if user_input.strip():
        add_message("You", user_input, align="right", color="#4961f6")
        response = get_response(user_input)
        add_message("Vita", response, align="left", color="#a7caff")
        user_entry.delete(0, tk.END)
    if user_input.lower() in ["quit", "bye"]:
        root.destroy()


# ------------------------
# GUI Setup
# ------------------------
root = tk.Tk()
root.title("Vita ChatBot")
root.geometry("440x650")
root.config(bg="#FFFFFF")

title_label = tk.Label(root, text="⌬ Vita Chatbot", font=("Helvetica", 18, "bold"),
                       fg="white", bg="#4961f6", pady=10)
title_label.pack(fill=tk.X)

chat_area_frame = tk.Frame(root, bg="white")  
chat_area_frame.pack(fill="both", expand=True, padx=10, pady=(10, 0))

chat_canvas = tk.Canvas(chat_area_frame, bg="white", highlightthickness=0)
scrollbar = tk.Scrollbar(chat_area_frame, orient="vertical", command=chat_canvas.yview)

chat_frame = tk.Frame(chat_canvas, bg="white")
chat_frame.bind("<Configure>", lambda e: chat_canvas.configure(scrollregion=chat_canvas.bbox("all")))

chat_window = chat_canvas.create_window((0, 0), window=chat_frame, anchor="nw")

def resize_chat_frame(event):
    chat_canvas.itemconfig(chat_window, width=event.width)

chat_canvas.bind("<Configure>", resize_chat_frame)
chat_canvas.configure(yscrollcommand=scrollbar.set)

chat_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

bottom_frame = tk.Frame(root, bg="#ffffff")
bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)

user_entry = tk.Entry(bottom_frame, font=("Arial", 14), relief="solid", bd=1, bg="#4961f6", fg="white")
user_entry.insert(0, "Help")
user_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
user_entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(
    bottom_frame, text="⌯⌲", bg="#4961f6", fg="white", font=("Arial", 15, "bold"),
    width=3, command=send_message
)
send_button.pack(side="right")

add_message("Vita", "Hello! I'm Vita, your assistant.", align="left", color="#a7caff")
add_message("Vita", "Type 'Help' to see what I can do.", align="left", color="#a7caff")

root.mainloop()
