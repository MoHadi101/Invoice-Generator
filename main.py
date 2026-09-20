# import tkinter
# from tkinter import ttk
# from docxtpl import DocxTemplate
# import datetime
# from tkinter import messagebox

# def clear_item():
#     qty_spinbox.delete(0, tkinter.END)
#     qty_spinbox.insert(0, "1")
#     desc_entry.delete(0, tkinter.END)
#     price_spinbox.delete(0, tkinter.END)
#     price_spinbox.insert(0, "0.0")

# invoice_list = []
# def add_item():
#     qty = int(qty_spinbox.get())
#     desc = desc_entry.get()
#     price = float(price_spinbox.get())
#     line_total = qty*price
#     invoice_item = [qty, desc, price, line_total]
#     tree.insert('',0, values=invoice_item)
#     clear_item()
    
#     invoice_list.append(invoice_item)

    
# def new_invoice():
#     first_name_entry.delete(0, tkinter.END)
#     last_name_entry.delete(0, tkinter.END)
#     phone_entry.delete(0, tkinter.END)
#     clear_item()
#     tree.delete(*tree.get_children())
    
#     invoice_list.clear()
    
# def generate_invoice():
#     doc = DocxTemplate("invoice_template.docx")
#     name = first_name_entry.get()+last_name_entry.get()
#     phone = phone_entry.get()
#     subtotal = sum(item[3] for item in invoice_list) 
#     salestax = 0.1
#     total = subtotal*(1-salestax)
    
#     doc.render({"name":name, 
#             "phone":phone,
#             "invoice_list": invoice_list,
#             "subtotal":subtotal,
#             "salestax":str(salestax*100)+"%",
#             "total":total})
    
#     doc_name = "new_invoice" + name + datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S") + ".docx"
#     doc.save(doc_name)
    
#     messagebox.showinfo("Invoice Complete", "Invoice Complete")
    
#     new_invoice()


    

# window = tkinter.Tk()
# window.title("Invoice Generator Form")

# frame = tkinter.Frame(window)
# frame.pack(padx=20, pady=10)

# first_name_label = tkinter.Label(frame, text="First Name")
# first_name_label.grid(row=0, column=0)
# last_name_label = tkinter.Label(frame, text="Last Name")
# last_name_label.grid(row=0, column=1)

# first_name_entry = tkinter.Entry(frame)
# last_name_entry = tkinter.Entry(frame)
# first_name_entry.grid(row=1, column=0)
# last_name_entry.grid(row=1, column=1)

# phone_label = tkinter.Label(frame, text="Phone")
# phone_label.grid(row=0, column=2)
# phone_entry = tkinter.Entry(frame)
# phone_entry.grid(row=1, column=2)

# qty_label = tkinter.Label(frame, text="Qty")
# qty_label.grid(row=2, column=0)
# qty_spinbox = tkinter.Spinbox(frame, from_=1, to=100)
# qty_spinbox.grid(row=3, column=0)

# desc_label = tkinter.Label(frame, text="Description")
# desc_label.grid(row=2, column=1)
# desc_entry = tkinter.Entry(frame)
# desc_entry.grid(row=3, column=1)

# price_label = tkinter.Label(frame, text="Unit Price")
# price_label.grid(row=2, column=2)
# price_spinbox = tkinter.Spinbox(frame, from_=0.0, to=500, increment=0.5)
# price_spinbox.grid(row=3, column=2)

# add_item_button = tkinter.Button(frame, text = "Add item", command = add_item)
# add_item_button.grid(row=4, column=2, pady=5)

# columns = ('qty', 'desc', 'price', 'total')
# tree = ttk.Treeview(frame, columns=columns, show="headings")
# tree.heading('qty', text='Qty')
# tree.heading('desc', text='Description')
# tree.heading('price', text='Unit Price')
# tree.heading('total', text="Total")

    
# tree.grid(row=5, column=0, columnspan=3, padx=20, pady=10)


# save_invoice_button = tkinter.Button(frame, text="Generate Invoice", command=generate_invoice)
# save_invoice_button.grid(row=6, column=0, columnspan=3, sticky="news", padx=20, pady=5)
# new_invoice_button = tkinter.Button(frame, text="New Invoice", command=new_invoice)
# new_invoice_button.grid(row=7, column=0, columnspan=3, sticky="news", padx=20, pady=5)


# window.mainloop()
import os
import sys
from tkinter import messagebox
import datetime
from docxtpl import DocxTemplate
import tkinter
from tkinter import ttk

# ------------------------------------------------------------
# HILFSFUNKTION: Pfad zum Icon (funktioniert im Skript und in der .exe)
# ------------------------------------------------------------
def resource_path(relative_path):
    """Ermittelt den Pfad zu einer Datei – funktioniert für Skript und für cx_Freeze-.exe."""
    if getattr(sys, 'frozen', False):
        # Bei cx_Freeze: die .exe liegt im Installationsordner, darin auch die eingebundenen Dateien
        base_path = os.path.dirname(sys.executable)
    else:
        # Normales Skript: aktueller Ordner
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
# ------------------------------------------------------------
# FUNKTIONEN (UNVERÄNDERT)
# ------------------------------------------------------------
def clear_item():
    qty_spinbox.delete(0, tkinter.END)
    qty_spinbox.insert(0, "1")
    desc_entry.delete(0, tkinter.END)
    price_spinbox.delete(0, tkinter.END)
    price_spinbox.insert(0, "0.0")

invoice_list = []

def add_item():
    qty = int(qty_spinbox.get())
    desc = desc_entry.get()
    price = float(price_spinbox.get())
    line_total = qty * price
    invoice_item = [qty, desc, price, line_total]
    tree.insert('', 0, values=invoice_item)
    clear_item()
    invoice_list.append(invoice_item)

def new_invoice():
    first_name_entry.delete(0, tkinter.END)
    last_name_entry.delete(0, tkinter.END)
    phone_entry.delete(0, tkinter.END)
    clear_item()
    tree.delete(*tree.get_children())
    invoice_list.clear()

def generate_invoice():
    try:
        output_dir = "invoices"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # --- 1. Vorlage mit absolutem Pfad laden (wichtig für .exe) ---
        template_path = resource_path("invoice_template.docx")
        doc = DocxTemplate(template_path)

        name = first_name_entry.get().strip() + " " + last_name_entry.get().strip()
        phone = phone_entry.get().strip()
        subtotal = sum(item[3] for item in invoice_list)
        salestax = 0.1
        total = subtotal * (1 - salestax)

        doc.render({
            "name": name,
            "phone": phone,
            "invoice_list": invoice_list,
            "subtotal": subtotal,
            "salestax": str(int(salestax * 100)) + "%",
            "total": total
        })

        doc_name = os.path.join(output_dir,
            "Rechnung_" + name.replace(" ", "_") +
            datetime.datetime.now().strftime("_%Y-%m-%d_%H%M%S") + ".docx"
        )
        doc.save(doc_name)

        messagebox.showinfo("Invoice Complete", f"Rechnung gespeichert unter:\n{doc_name}")
        new_invoice()

    except Exception as e:
        # Zeige den genauen Fehler in einer MessageBox an
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten:\n{str(e)}")
# ------------------------------------------------------------
# GUI – MODERNES, KLARES LAYOUT
# ------------------------------------------------------------
window = tkinter.Tk()
window.title("Invoice Generator")
window.geometry("780x650")
window.resizable(False, False)
window.configure(bg='#f0f2f5')   # heller Hintergrund

# Hauptframe (weiße Karte)
main_frame = tkinter.Frame(window, bg='white', bd=1, relief='solid',
                           highlightthickness=1, highlightcolor='#d0d7de')
main_frame.pack(padx=30, pady=25, fill='both', expand=True)

# Überschrift
title = tkinter.Label(main_frame, text="Rechnungsgenerator",
                      font=('Segoe UI', 18, 'bold'), bg='white', fg='#1a2634')
title.grid(row=0, column=0, columnspan=3, pady=(10, 20), sticky='w', padx=5)

# ---- Kundendaten ----
tkinter.Label(main_frame, text="Vorname", font=('Segoe UI', 10), bg='white', fg='#333').grid(row=1, column=0, sticky='w', padx=5)
tkinter.Label(main_frame, text="Nachname", font=('Segoe UI', 10), bg='white', fg='#333').grid(row=1, column=1, sticky='w', padx=5)
tkinter.Label(main_frame, text="Telefon", font=('Segoe UI', 10), bg='white', fg='#333').grid(row=1, column=2, sticky='w', padx=5)

first_name_entry = tkinter.Entry(main_frame, font=('Segoe UI', 10), bg='white', fg='#1a2634',
                                 relief='solid', bd=1, highlightthickness=0)
last_name_entry = tkinter.Entry(main_frame, font=('Segoe UI', 10), bg='white', fg='#1a2634',
                                relief='solid', bd=1, highlightthickness=0)
phone_entry = tkinter.Entry(main_frame, font=('Segoe UI', 10), bg='white', fg='#1a2634',
                            relief='solid', bd=1, highlightthickness=0)

first_name_entry.grid(row=2, column=0, padx=5, pady=(0,15), sticky='ew')
last_name_entry.grid(row=2, column=1, padx=5, pady=(0,15), sticky='ew')
phone_entry.grid(row=2, column=2, padx=5, pady=(0,15), sticky='ew')

# ---- Artikel hinzufügen ----
tkinter.Label(main_frame, text="Menge", font=('Segoe UI', 10), bg='white', fg='#333').grid(row=3, column=0, sticky='w', padx=5)
tkinter.Label(main_frame, text="Beschreibung", font=('Segoe UI', 10), bg='white', fg='#333').grid(row=3, column=1, sticky='w', padx=5)
tkinter.Label(main_frame, text="Stückpreis (€)", font=('Segoe UI', 10), bg='white', fg='#333').grid(row=3, column=2, sticky='w', padx=5)

qty_spinbox = tkinter.Spinbox(main_frame, from_=1, to=100, font=('Segoe UI', 10),
                              bg='white', fg='#1a2634', relief='solid', bd=1, width=10)
desc_entry = tkinter.Entry(main_frame, font=('Segoe UI', 10), bg='white', fg='#1a2634',
                           relief='solid', bd=1)
price_spinbox = tkinter.Spinbox(main_frame, from_=0.0, to=500, increment=0.5,
                                font=('Segoe UI', 10), bg='white', fg='#1a2634',
                                relief='solid', bd=1, width=10)

qty_spinbox.grid(row=4, column=0, padx=5, pady=(0,10), sticky='ew')
desc_entry.grid(row=4, column=1, padx=5, pady=(0,10), sticky='ew')
price_spinbox.grid(row=4, column=2, padx=5, pady=(0,10), sticky='ew')

# Add-Button (ttk mit Style)
add_btn = ttk.Button(main_frame, text="+ Artikel hinzufügen", command=add_item)
add_btn.grid(row=5, column=0, columnspan=3, pady=(5,15), sticky='ew')

# ---- Tabelle ----
columns = ('qty', 'desc', 'price', 'total')
tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=8)
tree.heading('qty', text='Menge')
tree.heading('desc', text='Beschreibung')
tree.heading('price', text='Stückpreis (€)')
tree.heading('total', text='Gesamt (€)')

tree.column('qty', width=70, anchor='center')
tree.column('desc', width=200, anchor='w')
tree.column('price', width=100, anchor='e')
tree.column('total', width=100, anchor='e')

tree.grid(row=6, column=0, columnspan=3, pady=(0,15), sticky='nsew')

# ---- Aktions-Buttons ----
btn_frame = tkinter.Frame(main_frame, bg='white')
btn_frame.grid(row=7, column=0, columnspan=3, sticky='ew', pady=5)
btn_frame.columnconfigure(0, weight=1)
btn_frame.columnconfigure(1, weight=1)

generate_btn = ttk.Button(btn_frame, text="Rechnung generieren", command=generate_invoice)
generate_btn.grid(row=0, column=0, padx=5, sticky='ew')

new_btn = ttk.Button(btn_frame, text="Neue Rechnung", command=new_invoice)
new_btn.grid(row=0, column=1, padx=5, sticky='ew')

# ------------------------------------------------------------
# STYLE FÜR TTK-WIDGETS
# ------------------------------------------------------------
style = ttk.Style()
style.theme_use('clam')

style.configure('TButton', font=('Segoe UI', 10), padding=6,
                borderwidth=0, focusthickness=0, focuscolor='none')
style.configure('TButton', background='#e1e8ed', foreground='#1a2634')
style.map('TButton', background=[('active', '#d0d7de'), ('pressed', '#c0c7ce')])

# Akzent für den Generieren-Button
style.configure('Accent.TButton', background='#2b7de9', foreground='white')
style.map('Accent.TButton', background=[('active', '#1a6bc4'), ('pressed', '#0f5aa0')])
generate_btn.config(style='Accent.TButton')

# Treeview
style.configure('Treeview', font=('Segoe UI', 9), rowheight=30,
                background='white', fieldbackground='white', foreground='#1a2634')
style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'),
                background='#e9ecf0', foreground='#1a2634', padding=5)
style.map('Treeview', background=[('selected', '#c7d8f0')])

# ------------------------------------------------------------
# GEWICHTUNG DER SPALTEN
# ------------------------------------------------------------
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.columnconfigure(2, weight=1)

# Fenster zentrieren
window.update_idletasks()
w = window.winfo_width()
h = window.winfo_height()
x = (window.winfo_screenwidth() // 2) - (w // 2)
y = (window.winfo_screenheight() // 2) - (h // 2)
window.geometry(f"{w}x{h}+{x}+{y}")

icon_path = resource_path("icon.ico")
window.iconbitmap(icon_path)

window.mainloop()