import tkinter as tk
from tkinter import scrolledtext
from lexer import lexer
from parser import Parser
from interpreter import Interpreter
import sys
import io

# --- Colors (One Dark Inspired) ---
BG_COLOR = "#282C34"
EDITOR_BG = "#1E2227"
TEXT_COLOR = "#ABB2BF"
TITLE_COLOR = "#E5C07B"
BTN_RUN = "#98C379"
BTN_CLEAR = "#E06C75"
BTN_TEXT = "#282C34"
CONSOLE_BG = "#1E1E1E"
CONSOLE_FG = "#98C379"
ERROR_FG = "#E06C75"


def run_code():
    code = code_box.get("1.0", tk.END)

    try:
        tokens = lexer(code)
        parser = Parser(tokens)
        ast = parser.parse()

        interpreter = Interpreter()

        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()

        interpreter.execute(ast)

        sys.stdout = old_stdout

        output_box.config(state="normal")
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, mystdout.getvalue())
        output_box.config(fg=CONSOLE_FG)
        output_box.config(state="disabled")

    except Exception as e:
        output_box.config(state="normal")
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, "❌ Error:\n" + str(e))
        output_box.config(fg=ERROR_FG)
        output_box.config(state="disabled")


def clear_code():
    code_box.delete("1.0", tk.END)
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.config(state="disabled")


# ---------------- GUI ----------------

window = tk.Tk()
window.title("Mini Script Compiler IDE")
window.geometry("950x750")
window.configure(bg=BG_COLOR)

title = tk.Label(
    window,
    text="Mini Script Compiler",
    font=("Segoe UI", 24, "bold"),
    bg=BG_COLOR,
    fg=TITLE_COLOR
)
title.pack(pady=(20, 10))

# Code editor label
editor_frame = tk.Frame(window, bg=BG_COLOR)
editor_frame.pack(padx=30, fill="x")

code_label = tk.Label(
    editor_frame,
    text="📝 Code Editor",
    font=("Segoe UI", 12, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
code_label.pack(anchor="w")

# Code editor
code_box = scrolledtext.ScrolledText(
    editor_frame,
    height=15,
    font=("Consolas", 14),
    bg=EDITOR_BG,
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    relief="flat",
    padx=10,
    pady=10
)
code_box.pack(fill="x", pady=5)

# Buttons frame
button_frame = tk.Frame(window, bg=BG_COLOR)
button_frame.pack(pady=10)

run_btn = tk.Button(
    button_frame,
    text="▶ Run Code",
    command=run_code,
    bg=BTN_RUN,
    fg=BTN_TEXT,
    font=("Segoe UI", 12, "bold"),
    width=15,
    relief="flat",
    cursor="hand2"
)
run_btn.grid(row=0, column=0, padx=15)

clear_btn = tk.Button(
    button_frame,
    text="🗑 Clear Code",
    command=clear_code,
    bg=BTN_CLEAR,
    fg=BTN_TEXT,
    font=("Segoe UI", 12, "bold"),
    width=15,
    relief="flat",
    cursor="hand2"
)
clear_btn.grid(row=0, column=1, padx=15)

output_frame = tk.Frame(window, bg=BG_COLOR)
output_frame.pack(padx=30, fill="x")

# Output label
output_label = tk.Label(
    output_frame,
    text="💻 Output Console",
    font=("Segoe UI", 12, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
output_label.pack(anchor="w")

# Output console
output_box = scrolledtext.ScrolledText(
    output_frame,
    height=10,
    font=("Consolas", 13),
    bg=CONSOLE_BG,
    fg=CONSOLE_FG,
    relief="flat",
    padx=10,
    pady=10
)
output_box.pack(fill="x", pady=5)

output_box.config(state="disabled")

window.mainloop()
