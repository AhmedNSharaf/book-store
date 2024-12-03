import tkinter as tk
from tkinter import messagebox
import sqlite3
from center_window import center_window
# Connect to the SQLite database
DATABASE = 'user_data.db'

def execute_query(query, params=()):
    """Helper function to execute a query on the database."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        #conn.close()
        return cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return None

# Add Book
def add_book():
    def submit():
        isbn = isbn_entry.get()
        title = title_entry.get()
        author = author_entry.get()
        genre = genre_entry.get()
        publication = publication_entry.get()
        price = float(price_entry.get())
        query = '''INSERT INTO Books (ISBN, Title, Author, Genre, Publication, Price) VALUES (?, ?, ?, ?, ?, ?)'''
        execute_query(query, (isbn, title, author, genre, publication, price))
        messagebox.showinfo("Success", "Book Added Successfully!")
        add_book_window.destroy()

    add_book_window = tk.Toplevel(control_window)
    add_book_window.title("Add Book")
    center_window(add_book_window,400,400)

    tk.Label(add_book_window, text="ISBN:").pack()
    isbn_entry = tk.Entry(add_book_window)
    isbn_entry.pack()

    tk.Label(add_book_window, text="Title:").pack()
    title_entry = tk.Entry(add_book_window)
    title_entry.pack()

    tk.Label(add_book_window, text="Author:").pack()
    author_entry = tk.Entry(add_book_window)
    author_entry.pack()

    tk.Label(add_book_window, text="Genre:").pack()
    genre_entry = tk.Entry(add_book_window)
    genre_entry.pack()

    tk.Label(add_book_window, text="Publication:").pack()
    publication_entry = tk.Entry(add_book_window)
    publication_entry.pack()

    tk.Label(add_book_window, text="Price:").pack()
    price_entry = tk.Entry(add_book_window)
    price_entry.pack()

    tk.Button(add_book_window, text="Submit", bg="green",command=submit).pack()

# Remove Book
def remove_book():
    def submit():
        isbn = isbn_entry.get()
        query = '''DELETE FROM Books WHERE ISBN = ?'''
        execute_query(query, (isbn,))
        messagebox.showinfo("Success", "Book Removed Successfully!")
        remove_book_window.destroy()

    remove_book_window = tk.Toplevel(control_window)
    remove_book_window.title("Remove Book")
    center_window(remove_book_window,400,400)

    tk.Label(remove_book_window, text="ISBN:").pack()
    isbn_entry = tk.Entry(remove_book_window)
    isbn_entry.pack()

    tk.Button(remove_book_window, text="Submit",bg="green", command=submit).pack()

# Update Book
def update_book():
    def submit():
        isbn = isbn_entry.get()
        field = field_entry.get()
        value = value_entry.get()
        query = f'''UPDATE Books SET {field} = ? WHERE ISBN = ?'''
        execute_query(query, (value, isbn))
        messagebox.showinfo("Success", "Book Updated Successfully!")
        update_book_window.destroy()

    update_book_window = tk.Toplevel(control_window)
    update_book_window.title("Update Book")
    center_window(update_book_window, 400, 250)


    tk.Label(update_book_window, text="ISBN:").pack()
    isbn_entry = tk.Entry(update_book_window)
    isbn_entry.pack()

    tk.Label(update_book_window, text="Field to Update (e.g., Title, Price):").pack()
    field_entry = tk.Entry(update_book_window)
    field_entry.pack()

    tk.Label(update_book_window, text="New Value:").pack()
    value_entry = tk.Entry(update_book_window)
    value_entry.pack()

    tk.Button(update_book_window, text="Submit",bg="green", command=submit).pack()

# Create User
def create_user():
    def submit():
        username = username_entry.get()
        password = password_entry.get()
        email = email_entry.get()
        balance = float(balance_entry.get())
        query = '''INSERT INTO users (username, password, email, balance) VALUES (?, ?, ?, ?)'''
        execute_query(query, (username, password, email, balance))
        messagebox.showinfo("Success", "User Created Successfully!")
        create_user_window.destroy()

    create_user_window = tk.Toplevel(control_window)
    create_user_window.title("Create User")
    center_window(create_user_window, 400, 250)


    tk.Label(create_user_window, text="Username:").pack()
    username_entry = tk.Entry(create_user_window)
    username_entry.pack()

    tk.Label(create_user_window, text="Password:").pack()
    password_entry = tk.Entry(create_user_window)
    password_entry.pack()

    tk.Label(create_user_window, text="Email:").pack()
    email_entry = tk.Entry(create_user_window)
    email_entry.pack()

    tk.Label(create_user_window, text="Balance:").pack()
    balance_entry = tk.Entry(create_user_window)
    balance_entry.pack()

    tk.Button(create_user_window, text="Submit",bg="green", command=submit).pack()

# Delete User
def delete_user():
    def submit():
        username = username_entry.get()
        query = '''DELETE FROM users WHERE username = ?'''
        execute_query(query, (username,))
        messagebox.showinfo("Success", "User Deleted Successfully!")
        delete_user_window.destroy()

    delete_user_window = tk.Toplevel(control_window)
    delete_user_window.title("Delete User")
    center_window(delete_user_window, 300, 200)


    tk.Label(delete_user_window, text="Username:").pack()
    username_entry = tk.Entry(delete_user_window)
    username_entry.pack()

    tk.Button(delete_user_window, text="Submit",bg="green", command=submit).pack()

# Create Admin User
def create_admin_user():
    def submit():
        admin_username = username_entry.get()
        admin_password = password_entry.get()
        admin_key = admin_key_entry.get()

        query = '''INSERT INTO Admins (username, password, admin_key ) VALUES (?, ?, ?)'''
        execute_query(query, (admin_username, admin_password, admin_key,))
        messagebox.showinfo("Success", "Admin User Created Successfully!")
        create_admin_window.destroy()

    create_admin_window = tk.Toplevel(control_window)
    create_admin_window.title("Create Admin User")
    center_window(create_admin_window, 400, 250)

    tk.Label(create_admin_window, text="Username:").pack()
    username_entry = tk.Entry(create_admin_window)
    username_entry.pack()

    tk.Label(create_admin_window, text="Password:").pack()
    password_entry = tk.Entry(create_admin_window, show="*")
    password_entry.pack()

    tk.Label(create_admin_window, text="admin key").pack()
    admin_key_entry = tk.Entry(create_admin_window)
    admin_key_entry.pack()

    

    tk.Button(create_admin_window, text="Submit", bg="green", command=submit).pack()

# Create Order
def create_order():
    def submit():
        order_date = order_date_entry.get()
        delivery_date = delivery_date_entry.get()
        total_cost = float(total_cost_entry.get())
        query = '''INSERT INTO Orders (Order_Date, Delivery_Date, Total_Cost) VALUES (?, ?, ?)'''
        execute_query(query, (order_date, delivery_date, total_cost))
        messagebox.showinfo("Success", "Order Created Successfully!")
        create_order_window.destroy()

    create_order_window = tk.Toplevel(control_window)
    create_order_window.title("Create Order")
    center_window(create_order_window, 400, 250)


    tk.Label(create_order_window, text="Order Date:").pack()
    order_date_entry = tk.Entry(create_order_window)
    order_date_entry.pack()

    tk.Label(create_order_window, text="Delivery Date:").pack()
    delivery_date_entry = tk.Entry(create_order_window)
    delivery_date_entry.pack()

    tk.Label(create_order_window, text="Total Cost:").pack()
    total_cost_entry = tk.Entry(create_order_window)
    total_cost_entry.pack()

    tk.Button(create_order_window, text="Submit", bg="green",command=submit).pack()

# Management Page Function
# Management Page Function
def create_management_page():
    global control_window
    control_window = tk.Tk()
    control_window.title("Database Management")
    center_window(control_window, 500, 500)

    button_width = 20  # Set a consistent width for all buttons
    button_height = 2  # Set a consistent height for better aesthetics
    pady = 10  # Set padding between buttons
    def logout():
        control_window.destroy()
        from registration import create_registration_screen
        create_registration_screen()
    tk.Button(control_window, text="Add Book", width=button_width, height=button_height, command=add_book).pack(pady=pady)
    tk.Button(control_window, text="Remove Book", width=button_width, height=button_height, command=remove_book).pack(pady=pady)
    tk.Button(control_window, text="Update Book", width=button_width, height=button_height, command=update_book).pack(pady=pady)
    tk.Button(control_window, text="Create User", width=button_width, height=button_height, command=create_user).pack(pady=pady)
    tk.Button(control_window, text="Delete User", width=button_width, height=button_height, command=delete_user).pack(pady=pady)
    tk.Button(control_window, text="Create Order", width=button_width, height=button_height, command=create_order).pack(pady=pady)
    tk.Button(control_window, text="Create Admin User", width=button_width, height=button_height, command=create_admin_user).pack(pady=pady)
    tk.Button(control_window, text="Log Out",bg="black",fg="white", width=button_width, height=button_height, command=logout).pack(pady=pady)
    

    control_window.mainloop()

    

