# main.py

import tkinter as tk
from tkinter import filedialog
from utils.pdf_processor import extract_metadata_from_pdf
import pandas as pd
import os
from styles import setup_treeview_style, create_widgets

# Determine the absolute path for the icon
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(BASE_DIR, 'app_icon.ico')

def select_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    for file_path in file_paths:
        metadata = extract_metadata_from_pdf(file_path)
        item_id = treeview.insert("", "end", values=(file_path, metadata))
        
        if "Title Unknown" in metadata:
            treeview.item(item_id, tags='problematic')
    treeview.tag_configure('problematic', foreground='red')

def deep_analysis():
    # Placeholder for deeper PDF analysis
    pass

# Right-click to Copy Functionality
def copy_title_to_clipboard(event=None):
    selected_items = treeview.selection()
    if not selected_items:
        return
    selected_item = selected_items[0]
    title = treeview.item(selected_item, "values")[1].split('-')[0]  # Splitting the metadata and extracting title
    app.clipboard_clear()
    app.clipboard_append(title)
    app.update()

def display_context_menu(event):
    context_menu.post(event.x_root, event.y_root)

# Export to Excel Functionality
def export_to_excel():
    rows = []
    for item in treeview.get_children():
        rows.append(treeview.item(item, "values"))
    
    df = pd.DataFrame(rows, columns=["File Path", "File Name Estimate"])
    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if not save_path:
        return
    
    df.to_excel(save_path, index=False, engine='openpyxl')

app = tk.Tk()
app.title("PDF Analyzer")
app.iconbitmap(ICON_PATH)

style = setup_treeview_style()

treeview, context_menu = create_widgets(app, select_files, deep_analysis, display_context_menu, copy_title_to_clipboard, export_to_excel)

app.mainloop()
