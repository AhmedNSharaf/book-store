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
        # Create a popup window for selecting a book
        cart_window = tk.Toplevel()
        cart_window.title("Add to Cart")
        cart_window.geometry("400x250")
        cart_window.configure(bg="#FAF9F6")
    
        tk.Label(cart_window, text="Select a book to add to the cart:", font=("Arial", 12), bg="#FAF9F6").pack(pady=10)
    
        # Connect to the database to fetch books
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT ISBN, Title, Price FROM Books')
        books = cursor.fetchall()
        conn.close()
    
        # Create a dictionary to map book titles to their ISBN and price
        book_dict = {book[1]: (book[0], book[2]) for book in books}
    
        # Create a dropdown list with book titles
        book_dropdown = ttk.Combobox(cart_window, state="readonly", font=("Arial", 12), width=30)
        book_dropdown['values'] = list(book_dict.keys())
        book_dropdown.pack(pady=10)
    
        # Input field for quantity
        tk.Label(cart_window, text="Enter Quantity:", font=("Arial", 12), bg="#FAF9F6").pack(pady=5)
        quantity_entry = tk.Entry(cart_window, font=("Arial", 12), width=10, justify="center")
        quantity_entry.pack(pady=5)
    
        def handle_add_to_cart():
            selected_title = book_dropdown.get()
            quantity = quantity_entry.get()
    
            if not selected_title:
                messagebox.showerror("Error", "Please select a book.")
                return
    
            if not quantity.isdigit() or int(quantity) <= 0:
                messagebox.showerror("Error", "Please enter a valid quantity (greater than 0).")
                return
    
            quantity = int(quantity)
            isbn, price = book_dict[selected_title]
    
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()
    
            # Check if the book is already in the cart
            cursor.execute('SELECT Quantity FROM Cart WHERE ISBN = ?', (isbn,))
            existing = cursor.fetchone()
            if existing:
                # Update quantity if the book is already in the cart
                cursor.execute('UPDATE Cart SET Quantity = Quantity + ? WHERE ISBN = ?', (quantity, isbn))
            else:
                # Add the book to the cart with the specified quantity
                cursor.execute('INSERT INTO Cart (ISBN, Title, Quantity, Price) VALUES (?, ?, ?, ?)',
                               (isbn, selected_title, quantity, price))
            conn.commit()
            conn.close()
    
            messagebox.showinfo("Success", f"'{selected_title}' has been added to your cart (Quantity: {quantity}).")
            cart_window.destroy()  # Close the pop-up window
            load_cart()  # Refresh the cart display
    
        # Add button to confirm selection
        tk.Button(cart_window, text="Add to Cart", font=("Arial", 12), bg="#4CAF50", fg="white", command=handle_add_to_cart).pack(pady=20)
    
        # Center the popup window
        cart_window.update_idletasks()
        width = cart_window.winfo_width()
        height = cart_window.winfo_height()
        x = (cart_window.winfo_screenwidth() // 2) - (width // 2)
        y = (cart_window.winfo_screenheight() // 2) - (height // 2)
        cart_window.geometry(f"{width}x{height}+{x}+{y}")

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
