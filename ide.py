import os
os.environ["PATH"] += os.pathsep + r"C:\Users\pn125\Downloads\windows_10_cmake_Release_Graphviz-14.1.3-win64\Graphviz-14.1.3-win64\bin"

import tkinter as tk
from tkinter import scrolledtext
from lexer import lexer
from parser import Parser
from interpreter import Interpreter
from tree_visualizer import draw_ast

from PIL import Image, ImageTk
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


def show_tree(image_path):
    global tree_photo

    img = Image.open(image_path)

    max_width = 900
    max_height = 500

    img.thumbnail((max_width, max_height))

    tree_photo = ImageTk.PhotoImage(img)

    tree_canvas.delete("all")
    tree_canvas.config(scrollregion=(0, 0, img.width, img.height))
    tree_canvas.create_image(0, 0, anchor="nw", image=tree_photo)


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

        img_path, pdf_path = draw_ast(ast)

        show_tree(img_path)

        print("PDF saved at:", pdf_path)

        try:
            os.startfile(pdf_path)
        except:
            pass

    except Exception as e:
        sys.stdout = sys.__stdout__

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

    tree_canvas.delete("all")


# ---------------- GUI ----------------

window = tk.Tk()
window.title("Mini Script Compiler IDE")
window.geometry("1200x950")
window.configure(bg=BG_COLOR)

title = tk.Label(
    window,
    text="Mini Script Compiler IDE",
    font=("Segoe UI", 24, "bold"),
    bg=BG_COLOR,
    fg=TITLE_COLOR
)
title.pack(pady=(20, 10))

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

code_box = scrolledtext.ScrolledText(
    editor_frame,
    height=12,
    font=("Consolas", 14),
    bg=EDITOR_BG,
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    relief="flat",
    padx=10,
    pady=10
)
code_box.pack(fill="x", pady=5)

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
    text="🗑 Clear",
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

output_label = tk.Label(
    output_frame,
    text="💻 Output Console",
    font=("Segoe UI", 12, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
output_label.pack(anchor="w")

output_box = scrolledtext.ScrolledText(
    output_frame,
    height=8,
    font=("Consolas", 13),
    bg=CONSOLE_BG,
    fg=CONSOLE_FG,
    relief="flat",
    padx=10,
    pady=10
)
output_box.pack(fill="x", pady=5)
output_box.config(state="disabled")

tree_title = tk.Label(
    window,
    text="🌳 Parse Tree Visualization",
    font=("Segoe UI", 12, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
tree_title.pack(pady=(15, 5))

tree_frame = tk.Frame(window, bg="#FAFAFA", bd=0, relief="flat")
tree_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))

tree_canvas = tk.Canvas(
    tree_frame,
    bg="#FAFAFA",
    highlightthickness=0
)
tree_canvas.pack(side="left", fill="both", expand=True)

v_scroll = tk.Scrollbar(tree_frame, orient="vertical", command=tree_canvas.yview)
v_scroll.pack(side="right", fill="y")

h_scroll = tk.Scrollbar(window, orient="horizontal", command=tree_canvas.xview)
h_scroll.pack(fill="x", padx=30, pady=(0, 10))

tree_canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

window.mainloop()