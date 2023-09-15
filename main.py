import tkinter as tk
from tkinter import ttk, filedialog
from utils.pdf_processor import extract_title_from_pdf
import pandas as pd
import os

# Determine the absolute path for the icon
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(BASE_DIR, 'app_icon.ico')

def select_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    for file_path in file_paths:
        title = extract_title_from_pdf(file_path)
        item_id = treeview.insert("", "end", values=(file_path, title))
        
        # Check the title and adjust the color if necessary
        if title == "Title Unknown. It is not possible to estimate the title.":
            treeview.item(item_id, tags='problematic')
    treeview.tag_configure('problematic', foreground='red')

def deep_analysis():
    # Placeholder for deeper PDF analysis
    pass

def copy_title_to_clipboard(event=None):
    selected_items = treeview.selection()
    if not selected_items:
        return
    selected_item = selected_items[0]
    title = treeview.item(selected_item, "values")[1]
    app.clipboard_clear()
    app.clipboard_append(title)
    app.update()

def display_context_menu(event):
    context_menu.post(event.x_root, event.y_root)

def export_to_excel():
    rows = []
    for item in treeview.get_children():
        rows.append(treeview.item(item, "values"))
    
    df = pd.DataFrame(rows, columns=["File Path", "Title"])
    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if not save_path:
        return
    
    df.to_excel(save_path, index=False, engine='openpyxl')

app = tk.Tk()
app.title("PDF Analyzer")

# Set the application icon using the absolute path
app.iconbitmap(ICON_PATH)

style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 10, "bold", "underline"))

select_button = tk.Button(app, text="Basic Analysis PDF", command=select_files)
select_button.grid(row=0, column=0, padx=10, pady=20, sticky=tk.W)

deep_analysis_button = tk.Button(app, text="Deep Analysis PDF", command=deep_analysis)
deep_analysis_button.grid(row=0, column=1, padx=10, pady=20)

treeview = ttk.Treeview(app, columns=("File Path", "Title"), show="headings")
treeview.heading("File Path", text="File Path")
treeview.heading("Title", text="Title")
treeview.column("File Path", anchor=tk.W, stretch=tk.YES)
treeview.column("Title", anchor=tk.W, stretch=tk.YES)
treeview.grid(row=1, column=0, columnspan=2, padx=10, pady=20, sticky=tk.W+tk.E+tk.N+tk.S)
treeview.bind("<Button-3>", display_context_menu)

scrollbar = ttk.Scrollbar(app, orient="vertical", command=treeview.yview)
scrollbar.grid(row=1, column=2, sticky=tk.N+tk.S)
treeview.configure(yscrollcommand=scrollbar.set)

app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

context_menu = tk.Menu(app, tearoff=0)
context_menu.add_command(label="Copy", command=copy_title_to_clipboard)

export_button = tk.Button(app, text="Export to Excel", command=export_to_excel)
export_button.grid(row=2, column=0, padx=10, pady=20, sticky=tk.W, columnspan=2)

app.mainloop()
