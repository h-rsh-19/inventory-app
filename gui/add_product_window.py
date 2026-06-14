# gui/add_product_window.py

import tkinter as tk
from tkinter import messagebox
import sqlite3

def open_add_product_window():
    def add_product():
        values = (
            name_entry.get(), barcode_entry.get(), batch_entry.get(),
            category_entry.get(), size_entry.get(), color_entry.get(),
            float(cost_price_entry.get()), float(retail_price_entry.get()), float(wholesale_price_entry.get()),
            int(quantity_entry.get()), warehouse_entry.get(), section_entry.get()
        )

        conn = sqlite3.connect("db/inventory.db")
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO products 
        (name, barcode, batch, category, size, color, cost_price, retail_price, wholesale_price, quantity, warehouse, section)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', values)
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Product added successfully")
        window.destroy()

    window = tk.Toplevel()
    window.title("Add New Product")
    labels = ["Name", "Barcode", "Batch", "Category", "Size", "Color", "Cost Price", "Retail Price", "Wholesale Price", "Quantity", "Warehouse", "Section"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(window, text=label).grid(row=i, column=0, pady=5, padx=5, sticky="e")
        entry = tk.Entry(window)
        entry.grid(row=i, column=1, pady=5, padx=5)
        entries.append(entry)

    (
        name_entry, barcode_entry, batch_entry, category_entry,
        size_entry, color_entry, cost_price_entry, retail_price_entry,
        wholesale_price_entry, quantity_entry, warehouse_entry, section_entry
    ) = entries

    tk.Button(window, text="Add Product", command=add_product).grid(row=len(labels), columnspan=2, pady=10)
