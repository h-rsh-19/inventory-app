import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def open_manage_products():
    def load_products():
        tree.delete(*tree.get_children())
        cursor.execute("SELECT * FROM products")
        for row in cursor.fetchall():
            tags = ('low',) if row[10] < 10 else ('ok',)
            tree.insert("", "end", values=row, tags=tags)

    def delete_selected():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a product to delete")
            return
        pid = tree.item(selected)['values'][0]
        cursor.execute("DELETE FROM products WHERE id = ?", (pid,))
        conn.commit()
        load_products()

    def edit_selected():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a product to edit")
            return

        data = tree.item(selected)['values']
        open_edit_window(data)

    def open_edit_window(data):
        edit_win = tk.Toplevel(window)
        edit_win.title("Edit Product")
        fields = ["name", "barcode", "batch", "category", "size", "color",
                  "cost_price", "retail_price", "wholesale_price", "quantity", "warehouse", "section"]

        entries = []
        for i, field in enumerate(fields):
            tk.Label(edit_win, text=field.capitalize()).grid(row=i, column=0)
            ent = tk.Entry(edit_win)
            ent.grid(row=i, column=1)
            ent.insert(0, data[i+1])
            entries.append(ent)

        def save_changes():
            updated = [e.get() for e in entries]
            cursor.execute(f'''
                UPDATE products SET
                name=?, barcode=?, batch=?, category=?, size=?, color=?,
                cost_price=?, retail_price=?, wholesale_price=?, quantity=?, warehouse=?, section=?
                WHERE id=?
            ''', (*updated, data[0]))
            conn.commit()
            load_products()
            edit_win.destroy()

        tk.Button(edit_win, text="Save", command=save_changes).grid(row=len(fields), columnspan=2, pady=10)

    # GUI setup
    window = tk.Toplevel()
    window.title("Manage Products")
    window.geometry("1100x400")

    cols = ["ID", "Name", "Barcode", "Batch", "Category", "Size", "Color",
            "Cost", "Retail", "Wholesale", "Qty", "Warehouse", "Section"]

    tree = ttk.Treeview(window, columns=cols, show="headings")
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=85)

    tree.tag_configure('low', background='#ffcccc')  # light red for low stock
    tree.tag_configure('ok', background='#eaffea')   # light green

    tree.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    tk.Button(window, text="Edit Selected", command=edit_selected).grid(row=1, column=0, pady=10)
    tk.Button(window, text="Delete Selected", command=delete_selected).grid(row=1, column=1, pady=10)
    tk.Button(window, text="Refresh", command=load_products).grid(row=1, column=2, pady=10)

    conn = sqlite3.connect("db/inventory.db")
    cursor = conn.cursor()

    load_products()
