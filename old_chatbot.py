import tkinter as tk
from tkinter import scrolledtext

# Enhanced response logic
def get_response(user_input):
    user_input = user_input.lower()

    # Try solving math expressions
    try:
        if any(op in user_input for op in ["+", "-", "*", "/", "**", "%"]):
            result = eval(user_input)  
            # safe for simple math only
            
            return f"The answer is {result}"
    except:
        return "Sorry, I couldn't calculate that. Please try a valid math expression."

    responses = {
        "hello": "Hello! How can I help you today?",
        "vita": "Yes, How can I help you today?",
        "hi": "Hi there! How are you?",
        "how are you": "I'm just a bot, but I'm doing great! How about you?",
        "what is your name": "I'm Vita, your virtual assistant.",
        "who created you": "Nishit created me using Python and Tkinter!",
        "thank you": "You're welcome! 😊",
        "age": "I don't have an age like humans. I'm timeless! 😉",
        "joke": "Why did the computer go to the doctor? Because it caught a virus! 😄",
        "bye": "Goodbye! Have a nice day!",
        "quit": "Goodbye! Have a nice day!",

        # Company FAQs
        "what services do you offer": "We offer web development and AI solutions.",
        "where are you located": "Our head office is in Indore, India, but we serve clients globally.",
        "how can i contact you": "You can contact us via email at abcd@abc.com or call +91 9234567890.",
        "what is your working hours": "We work Monday to Friday, 10 AM to 7 PM IST.",
        "do you offer support": "Yes, we provide 24/7 support for our clients through chat, email, and phone.",
        "what technologies do you use": "We use PHP, JavaScript, React, Node.js, HTML, CSS and more for our solutions.",
        "how much does a project cost": "Project costs depend on requirements. Please contact us with your project details for a quote.",
        "how experienced is your team": "Our team has over 9 years of experience in software development and tech consulting.",
        "do you provide custom solutions": "Yes, all our solutions are tailored to the client's requirements."
    }

    # Special help command
    if user_input == "help":
        return (
            "Here are the things you can ask me:\n"
            "- Hello / Hi / Vita\n"
            "- How Are You\n"
            "- What Is Your Name\n"
            "- Who Created You\n"
            "- Thank You / Bye / Quit\n"
            "- Age / Joke\n"
            "- You Can Also A Claculator\n\n"
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

    # Check for keywords
    for key in responses:
        if key in user_input:
            return responses[key]

    return "Sorry, I don't understand that. Type 'Help' to see what I can answer."

# Function to handle sending message
def send_message():
    user_input = user_entry.get()
    if user_input.strip() != "":
        chat_area.config(state='normal')
        chat_area.insert(tk.END, "You: " + user_input + "\n")
        chat_area.insert(tk.END, "Vita: " + get_response(user_input) + "\n\n")
        chat_area.config(state='disabled')
        chat_area.yview(tk.END)  # Scroll to the bottom
        user_entry.delete(0, tk.END)
    if user_input == "quit" or user_input == "bye":
        root.quit()  
        # Close the window
        # root.destroy()

# GUI setup
root = tk.Tk()
root.title("Vita ChatBot")
root.geometry("500x600")
root.config(bg="#E6E6FA")

title_label = tk.Label(root, text="💬 Vita ChatBot", font=("Arial", 24), fg="white", bg="#6A5ACD")
title_label.pack(fill=tk.X)

chat_area = scrolledtext.ScrolledText(root, state='disabled', wrap=tk.WORD  ,bg="#F8F8FF", fg="#333333", font=("Arial", 12))
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

user_entry = tk.Entry(root, font=("Arial", 14))
user_entry.insert(0, "Help")  # <-- This line adds default text
user_entry.pack(padx=10, pady=10, fill=tk.X)
user_entry.bind("<Return>", lambda event: send_message())  # Send on Enter key

send_button = tk.Button(root, text="Send", bg="#6A5ACD", fg="white", font=("Arial", 12, "bold") ,command=send_message)
send_button.pack(pady=5)

# Startup message
chat_area.config(state='normal')
chat_area.insert(tk.END, "Vita: Hello! I'm Vita.\n")
chat_area.insert(tk.END, "Vita: Type 'Help' to see what I can do.\n\n")
chat_area.config(state='disabled')

root.mainloop()
