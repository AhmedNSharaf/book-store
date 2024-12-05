import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from center_window import center_window

DATABASE = 'user_data.db'


# Helper function to execute queries
def execute_query(query, params=()):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        result = cursor.fetchall()
        conn.close()
        return result
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return None


# Create Management Page
def create_management_page():
    global control_window
    control_window = tk.Tk()
    control_window.title("Database Management")
    # control_window.geometry("1000x700")
    center_window(control_window, 1000, 700)

    # Sidebar for Buttons
    sidebar = tk.Frame(control_window, bg="#2c3e50", width=200)
    sidebar.pack(side="left", fill="y")

    # Main Area for Reports
    main_area = tk.Frame(control_window, bg="#ecf0f1")
    main_area.pack(side="right", expand=True, fill="both")

    # Styling for Buttons
    button_style = {
        "bg": "#34495e",
        "fg": "white",
        "activebackground": "#1abc9c",
        "font": ("Arial", 12),
        "relief": "flat",
        "width": 20,
        "height": 2,
    }

    # Utility Function: Clear Main Area
    def clear_main_area():
        for widget in main_area.winfo_children():
            widget.destroy()

    # Add Book Functionality
    def add_book():
        def submit():
            isbn = isbn_entry.get()
            title = title_entry.get()
            author = author_entry.get()
            category = category_entry.get()
            publication = publication_entry.get()
            price = price_entry.get()
            query = '''INSERT INTO Books (ISBN, Title, Author, category, Publication, Price) VALUES (?, ?, ?, ?, ?, ?)'''
            execute_query(query, (isbn, title, author, category, publication, price))
            messagebox.showinfo("Success", "Book added successfully!")
            clear_main_area()

        clear_main_area()
        tk.Label(main_area, text="Add New Book", font=("Arial", 16), bg="#ecf0f1").pack(pady=8)
        tk.Label(main_area, text="ISBN:").pack()
        isbn_entry = tk.Entry(main_area)
        isbn_entry.pack()

        tk.Label(main_area, text="Title:").pack()
        title_entry = tk.Entry(main_area)
        title_entry.pack()

        tk.Label(main_area, text="Author:").pack()
        author_entry = tk.Entry(main_area)
        author_entry.pack()

        tk.Label(main_area, text="Category:").pack()
        category_entry = tk.Entry(main_area)
        category_entry.pack()

        tk.Label(main_area, text="Publication:").pack()
        publication_entry = tk.Entry(main_area)
        publication_entry.pack()

        tk.Label(main_area, text="Price:").pack()
        price_entry = tk.Entry(main_area)
        price_entry.pack()

        tk.Button(main_area, text="Submit", bg="#1abc9c", command=submit).pack(pady=8)

    # Remove Book Functionality
    def remove_book():
        def submit():
            isbn = isbn_entry.get()
            query = '''DELETE FROM Books WHERE ISBN = ?'''
            execute_query(query, (isbn,))
            messagebox.showinfo("Success", "Book removed successfully!")
            clear_main_area()

        clear_main_area()
        tk.Label(main_area, text="Remove Book", font=("Arial", 16), bg="#ecf0f1").pack(pady=8)
        tk.Label(main_area, text="ISBN:").pack()
        isbn_entry = tk.Entry(main_area)
        isbn_entry.pack()

        tk.Button(main_area, text="Submit", bg="#1abc9c", command=submit).pack(pady=8)

    # Update Book Functionality
    def update_book():
        def submit():
            isbn = isbn_entry.get()
            field = field_entry.get()
            value = value_entry.get()
            query = f'''UPDATE Books SET {field} = ? WHERE ISBN = ?'''
            execute_query(query, (value, isbn))
            messagebox.showinfo("Success", "Book updated successfully!")
            clear_main_area()

        clear_main_area()
        tk.Label(main_area, text="Update Book", font=("Arial", 16), bg="#ecf0f1").pack(pady=8)
        tk.Label(main_area, text="ISBN:").pack()
        isbn_entry = tk.Entry(main_area)
        isbn_entry.pack()

        tk.Label(main_area, text="Field to Update (e.g., Title, Price):").pack()
        field_entry = tk.Entry(main_area)
        field_entry.pack()

        tk.Label(main_area, text="New Value:").pack()
        value_entry = tk.Entry(main_area)
        value_entry.pack()

        tk.Button(main_area, text="Submit", bg="#1abc9c", command=submit).pack(pady=8)

    # View Users Report
    def view_users_report():
        clear_main_area()
        tk.Label(main_area, text="Users Report", font=("Arial", 16), bg="#ecf0f1").pack(pady=8)

        columns = ("ID", "Username", "Email", "Balance")
        tree = ttk.Treeview(main_area, columns=columns, show="headings", height=20)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
        tree.pack(fill="both", padx=8, pady=8)

        query = '''SELECT id, username, email, balance FROM users'''
        rows = execute_query(query)
        for row in rows:
            tree.insert("", "end", values=row)

    # Logout Functionality
    def logout():
        control_window.destroy()
        from registration import create_registration_screen
        create_registration_screen()
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
            clear_main_area()

        clear_main_area()
        tk.Label(main_area, text="Create New User", font=("Arial", 16), bg="#ecf0f1").pack(pady=8)

        tk.Label(main_area, text="Username:").pack()
        username_entry = tk.Entry(main_area)
        username_entry.pack()

        tk.Label(main_area, text="Password:").pack()
        password_entry = tk.Entry(main_area, show="*")
        password_entry.pack()

        tk.Label(main_area, text="Email:").pack()
        email_entry = tk.Entry(main_area)
        email_entry.pack()

        tk.Label(main_area, text="Balance:").pack()
        balance_entry = tk.Entry(main_area)
        balance_entry.pack()

        tk.Button(main_area, text="Submit", bg="#1abc9c", command=submit).pack(pady=8)
    def delete_user():
        def submit():
            username = username_entry.get()
            query = '''DELETE FROM users WHERE username = ?'''
            execute_query(query, (username,))
            messagebox.showinfo("Success", "User Deleted Successfully!")
            clear_main_area()

        clear_main_area()
        tk.Label(main_area, text="Delete User", font=("Arial", 16), bg="#ecf0f1").pack(pady=8)

        tk.Label(main_area, text="Username:").pack()
        username_entry = tk.Entry(main_area)
        username_entry.pack()

        tk.Button(main_area, text="Submit", bg="#e74c3c", command=submit).pack(pady=8)
    def create_admin_user():
        def submit():
            admin_username = username_entry.get()
            admin_password = password_entry.get()
            admin_key = admin_key_entry.get()

            query = '''INSERT INTO Admins (username, password, admin_key) VALUES (?, ?, ?)'''
            execute_query(query, (admin_username, admin_password, admin_key))
            messagebox.showinfo("Success", "Admin User Created Successfully!")
            clear_main_area()

        clear_main_area()
        tk.Label(main_area, text="Create Admin User", font=("Arial", 16), bg="#ecf0f1").pack(pady=8)

        tk.Label(main_area, text="Username:").pack()
        username_entry = tk.Entry(main_area)
        username_entry.pack()

        tk.Label(main_area, text="Password:").pack()
        password_entry = tk.Entry(main_area, show="*")
        password_entry.pack()

        tk.Label(main_area, text="Admin Key:").pack()
        admin_key_entry = tk.Entry(main_area)
        admin_key_entry.pack()

        tk.Button(main_area, text="Submit", bg="#1abc9c", command=submit).pack(pady=8)

    def create_order():
        def submit():
            # order_date = order_date_entry.get()
            delivery_date = delivery_date_entry.get()
            total_cost = float(total_cost_entry.get())
            query = '''INSERT INTO Orders (Order_Date, Delivery_Date, Total_Cost) VALUES (DATE("now"), ?, ?)'''
            execute_query(query, ( delivery_date, total_cost))
            messagebox.showinfo("Success", "Order Created Successfully!")
            clear_main_area()

        clear_main_area()
        tk.Label(main_area, text="Create Order", font=("Arial", 16), bg="#ecf0f1").pack(pady=8)

        # tk.Label(main_area, text="Order Date:").pack()
        # order_date_entry = tk.Entry(main_area)
        # order_date_entry.pack()

        tk.Label(main_area, text="Delivery Date:").pack()
        delivery_date_entry = tk.Entry(main_area)
        delivery_date_entry.pack()

        tk.Label(main_area, text="Total Cost:").pack()
        total_cost_entry = tk.Entry(main_area)
        total_cost_entry.pack()

        tk.Button(main_area, text="Submit", bg="#1abc9c", command=submit).pack(pady=8)


    def order_report():
        def fetch_orders():
            """Fetch and display orders from the database."""
            query = '''SELECT Order_ID, Order_Date, Delivery_Date, Total_Cost FROM Orders'''
            orders = execute_query(query)
            
            # Clear the listbox
            orders_listbox.delete(0, tk.END)
            
            for order in orders:
                orders_listbox.insert(
                    tk.END,
                    f"ID: {order[0]} | Date: {order[1]} | Delivery: {order[2]} | Total: {order[3]:.2f}"
                )
        
        def edit_delivery_date():
            """Edit the delivery date of a selected order."""
            selected = orders_listbox.curselection()
            if not selected:
                messagebox.showwarning("Warning", "Please select an order to edit!")
                return
            
            selected_order = orders_listbox.get(selected)
            order_id = int(selected_order.split("|")[0].split(":")[1].strip())
            
            def submit_edit():
                new_date = new_delivery_date_entry.get()
                query = '''UPDATE Orders SET Delivery_Date = ? WHERE Order_ID = ?'''
                execute_query(query, (new_date, order_id))
                messagebox.showinfo("Success", "Delivery date updated successfully!")
                fetch_orders()
                edit_window.destroy()

            # Create a small pop-up window for editing
            edit_window = tk.Toplevel(control_window)
            edit_window.title("Edit Delivery Date")
            center_window(edit_window, 300, 150)
            
            tk.Label(edit_window, text="New Delivery Date:").pack(pady=5)
            new_delivery_date_entry = tk.Entry(edit_window)
            new_delivery_date_entry.pack(pady=5)
            
            tk.Button(edit_window, text="Submit", bg="#1abc9c", command=submit_edit).pack(pady=5)

        clear_main_area()
        tk.Label(main_area, text="Order Report", font=("Arial", 16), bg="#ecf0f1").pack(pady=8)
        
        # Listbox to display orders
        orders_listbox = tk.Listbox(main_area, width=80, height=15)
        orders_listbox.pack(pady=8)
        
        tk.Button(main_area, text="Refresh", bg="#3498db", command=fetch_orders).pack(pady=4)
        tk.Button(main_area, text="Edit Delivery Date", bg="#1abc9c", command=edit_delivery_date).pack(pady=4)
        
        fetch_orders()  # Fetch and display orders when the function is loaded



    # Sidebar Buttons
    tk.Button(sidebar, text="Add Book", command=add_book, **button_style).pack(pady=8)
    tk.Button(sidebar, text="Remove Book", command=remove_book, **button_style).pack(pady=8)
    tk.Button(sidebar, text="Update Book", command=update_book, **button_style).pack(pady=8)
    tk.Button(sidebar, text="Create user", command= create_user, **button_style).pack(pady=8)
    tk.Button(sidebar, text="Delete Users", command=delete_user, **button_style).pack(pady=8)
    tk.Button(sidebar, text="Users Report", command=view_users_report, **button_style).pack(pady=8)
    tk.Button(sidebar, text="Create Order", command=create_order, **button_style).pack(pady=8)
    tk.Button(sidebar, text="Order Report", command=order_report, **button_style).pack(pady=8)
    tk.Button(sidebar, text="Create Admin", command=create_admin_user, **button_style).pack(pady=8)
    tk.Button(sidebar, text="Log Out", command=logout, **button_style).pack(pady=8)
    
    # Placeholder for Welcome Message in Main Area
    tk.Label(
        main_area,
        text="Welcome to the Database Management System",
        bg="#ecf0f1",
        font=("Arial", 16),
        fg="#2c3e50",
    ).pack(pady=20)

    control_window.mainloop()


# Call the Management Page
if __name__ == "__main__":
    create_management_page()
 