import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import simpledialog

from create_database import create_database


def create_cart_table():
    # Create a temporary table for the cart
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cart (
            Cart_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ISBN TEXT NOT NULL,
            Title TEXT,
            Quantity INTEGER NOT NULL DEFAULT 1,
            Price REAL,
            FOREIGN KEY (ISBN) REFERENCES Books (ISBN)
        )
    ''')
    conn.commit()
    conn.close()


def show_cart_page(main_frame):
    # Clear the main frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Cart Page Content
    cart_frame = tk.Frame(main_frame, bg="#FAF9F6")
    cart_frame.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(cart_frame, text="Your Cart", font=("Arial", 18, "bold"), bg="#FAF9F6").pack(pady=10)

    # Cart Table
    columns = ("ISBN", "Title", "Quantity", "Price", "Total")
    cart_table = ttk.Treeview(cart_frame, columns=columns, show="headings", height=10)
    for col in columns:
        cart_table.heading(col, text=col)
    cart_table.pack(pady=10, fill="x")

    # Function to fetch and display cart contents
    def load_cart():
        cart_table.delete(*cart_table.get_children())
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT ISBN, Title, Quantity, Price, Quantity * Price AS Total FROM Cart')
        for row in cursor.fetchall():
            cart_table.insert("", "end", values=row)
        conn.close()

    load_cart()

    # Function to add books to the cart
    def add_to_cart():
        isbn = simpledialog.askstring("Add to Cart", "Enter the ISBN of the book:")
        if isbn:
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()
            # Check if the book exists
            cursor.execute('SELECT Title, Price FROM Books WHERE ISBN = ?', (isbn,))
            book = cursor.fetchone()
            if book:
                title, price = book
                # Check if the book is already in the cart
                cursor.execute('SELECT Quantity FROM Cart WHERE ISBN = ?', (isbn,))
                existing = cursor.fetchone()
                if existing:
                    cursor.execute('UPDATE Cart SET Quantity = Quantity + 1 WHERE ISBN = ?', (isbn,))
                else:
                    cursor.execute('INSERT INTO Cart (ISBN, Title, Quantity, Price) VALUES (?, ?, ?, ?)',
                                   (isbn, title, 1, price))
                conn.commit()
                messagebox.showinfo("Success", f"'{title}' has been added to your cart.")
            else:
                messagebox.showerror("Error", "Book not found.")
            conn.close()
            load_cart()

    # Function to remove books from the cart
    def remove_from_cart():
        selected_item = cart_table.selection()
        if selected_item:
            isbn = cart_table.item(selected_item, "values")[0]
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Cart WHERE ISBN = ?', (isbn,))
            conn.commit()
            conn.close()
            load_cart()
            messagebox.showinfo("Removed", "Item removed from cart.")
        else:
            messagebox.showwarning("No Selection", "Please select an item to remove.")

    # Function to proceed to checkout
    def checkout():
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT SUM(Quantity * Price) FROM Cart')
        total_cost = cursor.fetchone()[0]
        if total_cost:
            # Insert a new order
            cursor.execute('INSERT INTO Orders (Order_Date, Total_Cost) VALUES (DATE("now"), ?)', (total_cost,))
            order_id = cursor.lastrowid
            conn.commit()
            conn.close()
            messagebox.showinfo("Checkout Successful", f"Order #{order_id} placed. Total cost: ${total_cost:.2f}")
            # Clear the cart
            clear_cart()
            load_cart()
        else:
            messagebox.showwarning("Empty Cart", "Your cart is empty.")

    # Function to clear the cart
    def clear_cart():
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Cart')
        conn.commit()
        conn.close()

    # Buttons
    button_frame = tk.Frame(cart_frame, bg="#FAF9F6")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Add to Cart", bg="#4CAF50", fg="white", font=("Arial", 12), command=add_to_cart).pack(
        side="left", padx=5)
    tk.Button(button_frame, text="Remove Selected", bg="#FF5722", fg="white", font=("Arial", 12),
              command=remove_from_cart).pack(side="left", padx=5)
    tk.Button(button_frame, text="Checkout", bg="#007BFF", fg="white", font=("Arial", 12), command=checkout).pack(
        side="left", padx=5)


# Create the database and cart table
create_database()
create_cart_table()
