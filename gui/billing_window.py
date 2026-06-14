# gui/billing_window.py

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from utils.pdf_generator import generate_invoice_pdf
from datetime import datetime

cart = []

def open_billing_window(username):
    def fetch_products():
        conn = sqlite3.connect("db/inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, wholesale_price, retail_price FROM products WHERE quantity > 0")
        items = cursor.fetchall()
        conn.close()
        return items

    def add_to_cart():
        product_id = product_var.get()
        qty = int(quantity_entry.get())
        price_type = price_type_var.get()

        for prod in products:
            if str(prod[0]) == product_id:
                name, wholesale_price, retail_price = prod[1], prod[2], prod[3]
                price = wholesale_price if price_type == "wholesale" else retail_price
                subtotal = qty * price
                cart.append((product_id, name, qty, price, subtotal, price_type))
                update_cart_view()
                return

    def update_cart_view():
        for row in cart_tree.get_children():
            cart_tree.delete(row)
        for item in cart:
            cart_tree.insert("", "end", values=(item[1], item[2], item[3], item[4], item[5]))

    def complete_sale():
        if not cart:
            messagebox.showerror("Error", "Cart is empty.")
            return

        conn = sqlite3.connect("db/inventory.db")
        cursor = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for item in cart:
            pid, _, qty, price, _, price_type = item

            cursor.execute("INSERT INTO sales (product_id, quantity, price_type, date) VALUES (?, ?, ?, ?)",
                           (pid, qty, price_type, now))
            cursor.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?", (qty, pid))

        conn.commit()
        conn.close()

        generate_invoice_pdf(cart, username)
        messagebox.showinfo("Success", "Sale completed and invoice generated.")
        cart.clear()
        update_cart_view()

    # GUI
    win = tk.Tk()
    win.title("Billing System")
    win.geometry("800x500")

    tk.Label(win, text="Product:").grid(row=0, column=0, padx=10, pady=10)
    product_var = tk.StringVar()
    product_dropdown = ttk.Combobox(win, textvariable=product_var, state="readonly", width=40)
    products = fetch_products()
    product_dropdown['values'] = [f"{p[0]} - {p[1]}" for p in products]
    product_dropdown.grid(row=0, column=1)

    tk.Label(win, text="Quantity:").grid(row=1, column=0, padx=10, pady=10)
    quantity_entry = tk.Entry(win)
    quantity_entry.grid(row=1, column=1)

    tk.Label(win, text="Price Type:").grid(row=2, column=0, padx=10, pady=10)
    price_type_var = tk.StringVar(value="retail")
    ttk.Combobox(win, textvariable=price_type_var, values=["retail", "wholesale"], state="readonly").grid(row=2, column=1)

    tk.Button(win, text="Add to Cart", command=add_to_cart).grid(row=3, column=1, pady=10)

    cart_tree = ttk.Treeview(win, columns=("Product", "Qty", "Price", "Subtotal", "Type"), show="headings")
    for col in cart_tree["columns"]:
        cart_tree.heading(col, text=col)
    cart_tree.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    tk.Button(win, text="Complete Sale & Generate Invoice", command=complete_sale).grid(row=5, column=1, pady=20)

    win.mainloop()
