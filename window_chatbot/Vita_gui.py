import tkinter as tk
import tkinter.font as tkFont
from datetime import datetime
from Vita_ML_Chatbot import get_response   # use chatbot brain

# -----------------------------
# GUI Helpers
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
# GUI Setup
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
