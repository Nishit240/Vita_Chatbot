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
        "hello": "Hello! How can I help you today?",
        "vita": "Yes, How can I help you today?",
        "hi": "Hi there! How are you?",
        "how are you": "I'm just a bot, but I'm doing great! How about you?",
        "your name": "I'm Vita, your virtual assistant.",
        "who created you": "Nishit created me using Python and Tkinter!",
        "thank you": "You're welcome! 😊",
        "age": "I don't have an age like humans. I'm timeless! 😉",
        "joke": "Why did the computer go to the doctor? Because it caught a virus! 😄",
        "bye": "Goodbye! Have a nice day!",
        "quit": "Goodbye! Have a nice day!",
        "ok": "Yes. Need any help? ",

        # Company FAQs
        "what services do you offer": "We offer web development and AI solutions.",
        "where are you located": "Our head office is in Indore, India, but we serve clients globally.",
        "contact": "You can contact us via email at abcd@abc.com or call +91 9234567890.",
        "working hours": "We work Monday to Friday, 10 AM to 7 PM IST.",
        "support": "Yes, we provide 24/7 support for our clients through chat, email, and phone.",
        "technologies do you use": "We use PHP, JavaScript, React, Node.js, HTML, CSS and more for our solutions.",
        "project cost": "Project costs depend on requirements. Please contact us with your project details for a quote.",
        "how experienced is your team": "Our team has over 9 years of experience in software development and tech consulting.",
        "provide custom solutions": "Yes, all our solutions are tailored to the client's requirements."
    }

    if user_input == "help":
        return (
            "Here are the things you can ask me:\n"
            "- Hello / Hi / Vita\n"
            "- How Are You\n"
            "- What Is Your Name\n"
            "- Who Created You\n"
            "- Thank You / Bye / Quit\n"
            "- Age / Joke\n"
            "- You Can Also A Calculator\n\n"
            "Company Faqs:\n"
            "- What Services Do You Offer\n"
            "- Where Are You Located\n"
            "- How Can I Contact You\n"
            "- What Is Your Working Hours\n"
            "- Do You Offer Support\n"
            "- What Technologies Do You Use\n"
            "- How Much Does A Project Cost\n"
            "- How Experienced Is Your Team\n"
            "- Do You Provide Custom Solutions\n"
        )

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
