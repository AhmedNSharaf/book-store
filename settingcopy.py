import sqlite3
import tkinter as tk
from tkinter import messagebox
import re  # For email validation
from create_management_page_original import execute_query

# At the top of setting.py


def get_user_data():
    from  registration  import user
    # conn = connect_db()
    # cursor = conn.cursor()
    # cursor.execute("SELECT first_name, last_name, email, password, username, phone_number, country FROM settings WHERE id = 1")
    # user_data = cursor.fetchone()
    # conn.close()
    query="SELECT username, password FROM users WHERE id  =?  "
    return execute_query(query, (user,))

def update_user_in_database( new_username, new_password  ):
     from  registration  import user
    # conn = connect_db()
    # cursor = conn.cursor()
    # cursor.execute("""
        # UPDATE settings 
        # SET first_name = ?, last_name = ?, username = ?, password = ?, phone_number = ?, country = ? 
        # WHERE id = ?""", (new_first_name, new_last_name, new_username, new_password, new_phone_number, new_country, 1))
    # conn.commit()
    # conn.close()
     query="""UPDATE users  SET  username = ?, password = ? WHERE username = ?"""
     return execute_query(query, (new_username,new_password,user))


# UI functions for settings
def show_settings_page(main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()

    settings_frame = tk.Frame(main_frame, bg="#FAF9F6")
    settings_frame.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(settings_frame, text="Settings", font=("Arial", 24, "bold"), bg="#FAF9F6", fg="#333").pack(pady=(10, 20))
    
    tk.Button(settings_frame, text="Update Username/Password", font=("Arial", 14), bg="#4CAF50", fg="white",
              command=lambda: show_update_account_page(main_frame)).pack(fill="x", padx=10, pady=5)
    tk.Button(settings_frame, text="Manage Payment Methods", font=("Arial", 14), bg="#4CAF50", fg="white",
              command=lambda: show_payment_methods_page(main_frame)).pack(fill="x", padx=10, pady=5)
    # tk.Button(settings_frame, text="View User Data", font=("Arial", 14), bg="#4CAF50", fg="white",
            #   command=show_user_data).pack(fill="x", padx=10, pady=5)

def show_update_account_page(main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()

    update_frame = tk.Frame(main_frame, bg="#FAF9F6")
    update_frame.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(update_frame, text="Update Username/Password", font=("Arial", 24, "bold"), bg="#FAF9F6", fg="#333").pack(pady=(10, 20))

    old_username_var = tk.StringVar()
    old_password_var = tk.StringVar()
    new_username_var = tk.StringVar()
    new_password_var = tk.StringVar()
    
    tk.Label(update_frame, text="Old Username:", font=("Arial", 14), bg="#FAF9F6", fg="#333").pack(anchor="w", pady=(5, 5))
    tk.Entry(update_frame, textvariable=old_username_var, font=("Arial", 12), bg="#FFFFFF").pack(anchor="w", padx=10, pady=(0, 10))

    tk.Label(update_frame, text="Old Password:", font=("Arial", 14), bg="#FAF9F6", fg="#333").pack(anchor="w", pady=(5, 5))
    tk.Entry(update_frame, textvariable=old_password_var, show='*', font=("Arial", 12), bg="#FFFFFF").pack(anchor="w", padx=10, pady=(0, 10))

    tk.Label(update_frame, text="New Username:", font=("Arial", 14), bg="#FAF9F6", fg="#333").pack(anchor="w", pady=(5, 5))
    tk.Entry(update_frame, textvariable=new_username_var, font=("Arial", 12), bg="#FFFFFF").pack(anchor="w", padx=10, pady=(0, 10))

    tk.Label(update_frame, text="New Password:", font=("Arial", 14), bg="#FAF9F6", fg="#333").pack(anchor="w", pady=(5, 5))
    tk.Entry(update_frame, textvariable=new_password_var, show='*', font=("Arial", 12), bg="#FFFFFF").pack(anchor="w", padx=10, pady=(0, 10))

    tk.Button(update_frame, text="Save Changes", font=("Arial", 14), bg="#4CAF50", fg="white",
              command=lambda: save_account_changes(old_username_var, old_password_var, new_username_var, new_password_var)).pack(pady=(20, 10), fill="x", padx=10)

    tk.Button(update_frame, text="Back", font=("Arial", 14), bg="#FF5722", fg="white",
              command=lambda: show_settings_page(main_frame)).pack(pady=4, fill="x", padx=10)

def save_account_changes(old_username_var, old_password_var, new_username_var, new_password_var):
    old_username = old_username_var.get().strip()
    old_password = old_password_var.get().strip()
    new_username = new_username_var.get().strip()
    new_password = new_password_var.get().strip()

    # Fetch current user details
    user_data = get_user_data()
    current_username = user_data[0][0] if user_data else None
    current_password = user_data[0][1] if user_data else None

    # Validate input
    if not all([old_username, old_password, new_username, new_password]):
        messagebox.showerror("Error", "All fields must be filled.")
        return

    # Validate old credentials
    if old_username != current_username or old_password != current_password:
        messagebox.showerror("Error", "Old username or password is incorrect.")
        return

    # Additional validation for new username and password
    if len(new_username) < 6:
        messagebox.showerror("Error", "New username must be at least 6 characters long.")
        return

    if len(new_password) < 6:
        messagebox.showerror("Error", "New password must be at least 6 characters long.")
        return

    # Update the database with new credentials
    try:
        update_user_in_database(new_username, new_password)
        messagebox.showinfo("Success", "Username and password updated successfully!")
        
        # Optionally redirect to the home page or reset fields
        show_home_page(new_username)

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while updating the account: {e}")

# def show_user_data():
    # user_data_window = tk.Toplevel(root)
    # user_data_window.title("User Data")
    # user_data_window.geometry("400x400")
    # 
    # user_data = get_user_data()
    # if user_data:
        # tk.Label(user_data_window, text=f"Name: {user_data[0]} {user_data[1]}").pack(anchor="w", padx=10, pady=5)
        # tk.Label(user_data_window, text=f"Email: {user_data[2]}").pack(anchor="w", padx=10, pady=5)
        # tk.Label(user_data_window, text=f"Username: {user_data[4]}").pack(anchor="w", padx=10, pady=5)
        # tk.Label(user_data_window, text=f"Phone Number: {user_data[5]}").pack(anchor="w", padx=10, pady=5)  # New field
        # tk.Label(user_data_window, text=f"Country: {user_data[6]}").pack(anchor="w", padx=10, pady=5)  # New field
    # else:
        # tk.Label(user_data_window, text="No user data found.").pack(pady=20)
# 
def show_home_page(username):
    # Function to display the home page with updated username
    print(f"Welcome, {username}!")  # Replace with actual home page fUI code

# Payment methods functions

def show_payment_methods_page(main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()

    payment_frame = tk.Frame(main_frame, bg="#FAF9F6")
    payment_frame.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(payment_frame, text="Payment Methods", font=("Arial", 24, "bold"), bg="#FAF9F6", fg="#333").pack(pady=(10, 20))

    # Predefined list of payment methods
    predefined_methods = ["Credit Card", "Debit Card", "PayPal", "Bank Transfer"]
    selected_method_var = tk.StringVar()

    tk.Label(payment_frame, text="Select Payment Method:", font=("Arial", 18, "bold"), bg="#FAF9F6", fg="#4CAF50").pack(anchor="w", pady=(10, 5))
    for method in predefined_methods:
        tk.Radiobutton(payment_frame, text=method, variable=selected_method_var, value=method, bg="#FAF9F6").pack(anchor="w", padx=10)

    tk.Button(payment_frame, text="Save Method", font=("Arial", 14), bg="#4CAF50", fg="white",
              command=lambda: save_payment_method(selected_method_var.get())).pack(pady=(10, 10), fill="x", padx=10)

    tk.Button(payment_frame, text="Back", font=("Arial", 14), bg="#FF5722", fg="white",
              command=lambda: show_settings_page(main_frame)).pack(pady=4, fill="x", padx=10)

def save_payment_method(method):
    if method:
        from registration import user
        query = """UPDATE users SET payment_method = ? WHERE username = ?"""
        execute_query(query, (method, user))
        messagebox.showinfo("Success", "Payment method saved successfully!")
    else:
        messagebox.showerror("Error", "Please select a payment method.")






def get_payment_methods():
    # conn = connect_db()
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM payment_methods")
    # methods = cursor.fetchall()
    # conn.close()
    query="""SELECT payment_method FROM users WHERE username=? """
    from  registration  import user
    return execute_query(query, (user,))

# 
def add_payment_method(method):
    if method:
        from  registration  import user
        # conn = connect_db()
        # cursor = conn.cursor()
        # cursor.execute("INSERT INTO payment_methods (method) VALUES (?)", (method,))
        # conn.commit()
        # conn.close()
        # messagebox.showinfo("Success", "Payment method added successfully!")
        query="""UPDATE users  SET  payment_method = ? WHERE username = ?"""
        execute_query(query, (method,user,))
    else:
        messagebox.showerror("Error", "Payment method cannot be empty!")



def show_page(page_function, main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()  # Remove existing widgets
    page_function(main_frame)
# Main application loop
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Book Store Application")
    root.geometry("800x600")
    
    show_settings_page(root)  # Start on settings page
    root.mainloop()