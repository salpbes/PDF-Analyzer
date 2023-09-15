# styles.py

import tkinter as tk
from tkinter import ttk

def setup_treeview_style():
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 10, "bold", "underline"))
    return style

def create_widgets(app, select_files, deep_analysis, display_context_menu, copy_title_to_clipboard, export_to_excel):
    basic_analysis_button = tk.Button(app, text="Basic Analysis PDF", command=select_files)
    basic_analysis_button.grid(row=0, column=0, padx=10, pady=20, sticky=tk.W)

    deep_analysis_button = tk.Button(app, text="Deep Analysis PDF", command=deep_analysis)
    deep_analysis_button.grid(row=0, column=1, padx=10, pady=20)

    treeview = ttk.Treeview(app, columns=("File Path", "File Name Estimate"), show="headings")
    treeview.heading("File Path", text="File Path")
    treeview.heading("File Name Estimate", text="File Name Estimate")
    treeview.column("File Path", anchor=tk.W, stretch=tk.YES)
    treeview.column("File Name Estimate", anchor=tk.W, stretch=tk.YES)
    treeview.grid(row=1, column=0, columnspan=2, padx=10, pady=20, sticky=tk.W+tk.E+tk.N+tk.S)
    treeview.bind("<Button-3>", display_context_menu)

    scrollbar = ttk.Scrollbar(app, orient="vertical", command=treeview.yview)
    scrollbar.grid(row=1, column=2, sticky=tk.N+tk.S)
    treeview.configure(yscrollcommand=scrollbar.set)

    context_menu = tk.Menu(app, tearoff=0)
    context_menu.add_command(label="Copy", command=copy_title_to_clipboard)

    export_button = tk.Button(app, text="Export to Excel", command=export_to_excel)
    export_button.grid(row=2, column=0, padx=10, pady=20, sticky=tk.W, columnspan=2)

    return treeview, context_menu  # Return widgets that you need to reference later
