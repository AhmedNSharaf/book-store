def setting_page(main_frame,user):
    import sqlite3
    import tkinter as tk
    from tkinter import messagebox
    import re  # For email validation
    from create_management_page import execute_query
    # from global_var import user_instance
    global user_instance
    user_instance = user

    def get_user_data(user_id):
        global user
        print(user_instance)
        query = "SELECT username, password FROM users WHERE id  =?"
        print("user=", user_instance)
        return execute_query(query, (user_id,))

    def update_user_in_database(new_username, new_password, user_id):
        query = """UPDATE users  SET  username = ?, password = ? WHERE id = ?"""
        return execute_query(query, (new_username, new_password, user_id))

    def show_settings_page(main_frame, user_id):
        for widget in main_frame.winfo_children():
            widget.destroy()

        settings_frame = tk.Frame(main_frame, bg="#FAF9F6")
        settings_frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(settings_frame, text="Settings", font=("Arial", 24, "bold"), bg="#FAF9F6", fg="#333").pack(pady=(10, 20))

        tk.Button(settings_frame, text="Update Username/Password", font=("Arial", 14), bg="#4CAF50", fg="white",
                  command=lambda: show_update_account_page(main_frame, user_id)).pack(fill="x", padx=10, pady=5)
        tk.Button(settings_frame, text="Manage Payment Methods", font=("Arial", 14), bg="#4CAF50", fg="white",
                  command=lambda: show_payment_methods_page(main_frame)).pack(fill="x", padx=10, pady=5)

    def show_update_account_page(main_frame, user_id):
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
                  command=lambda: save_account_changes(user_id, old_username_var, old_password_var, new_username_var, new_password_var)).pack(pady=(20, 10), fill="x", padx=10)

        tk.Button(update_frame, text="Back", font=("Arial", 14), bg="#FF5722", fg="white",
                  command=lambda: setting_page(main_frame,user)).pack(pady=4, fill="x", padx=10)

    def save_account_changes(user_id, old_username_var, old_password_var, new_username_var, new_password_var):
        old_username = old_username_var.get()
        old_password = old_password_var.get()
        new_username = new_username_var.get()
        new_password = new_password_var.get()
        var = get_user_data(user_id)
        current_user = var[0]

        current_username = current_user[0] if current_user else None
        current_password = current_user[1] if current_user else None

        if not all([old_username, old_password, new_username, new_password]):
            messagebox.showerror("Error", "All fields must be filled.")
            return

        if old_username != current_username or old_password != current_password:
            messagebox.showerror("Error", "Old username or password is incorrect.")
            return

        if len(new_username) < 6:
            messagebox.showerror("Error", "New username must be at least 6 characters long.")
            return

        if len(new_password) < 6:
            messagebox.showerror("Error", "New password must be at least 6 characters long.")
            return

        try:
            update_user_in_database(new_username, new_password, user_id)
            messagebox.showinfo("Success", "Username and Password updated successfully!")

            # Clear input fields
            old_username_var.set("")
            old_password_var.set("")
            new_username_var.set("")
            new_password_var.set("")

            show_home_page(new_username)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred while updating your account: {e}")

    def show_home_page(username):
        print(f"Welcome, {username}!")

    def show_payment_methods_page(main_frame):
        from tkinter.ttk import Combobox  # Import Combobox from tkinter.ttk

        def update_payment_method_label():
            # Fetch the current payment method and update the label
            payment_methods = get_payment_methods()
            if payment_methods and payment_methods[0]:
                current_method = payment_methods[0][0]  # Assuming payment_methods is a list of tuples
                payment_method_label.config(text=f"Current Payment Method: {current_method}")
            else:
                payment_method_label.config(text="No payment method selected.")

        for widget in main_frame.winfo_children():
            widget.destroy()

        payment_frame = tk.Frame(main_frame, bg="#FAF9F6")
        payment_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Label for displaying the current payment method
        global payment_method_label
        payment_method_label = tk.Label(payment_frame, text="Current Payment Method: None",
                                        font=("Arial", 14, "bold"), bg="#FAF9F6", fg="#333")
        payment_method_label.pack(anchor="w", padx=10, pady=(10, 20))

        # Update the label to display the latest payment method
        update_payment_method_label()

        tk.Label(payment_frame, text="Add New Payment Method:", font=("Arial", 18, "bold"),
                bg="#FAF9F6", fg="#4CAF50").pack(anchor="w", pady=(10, 5))

        # Define the available payment methods
        available_methods = ["Credit Card", "Debit Card", "PayPal", "Bank Transfer", "UPI"]

        # Create a Combobox for selecting payment methods
        global new_method_var
        new_method_var = tk.StringVar()
        method_dropdown = Combobox(payment_frame, textvariable=new_method_var, font=("Arial", 12), state="readonly")
        method_dropdown['values'] = available_methods  # Set the drop-down options
        method_dropdown.pack(anchor="w", padx=10, pady=(0, 10))

        tk.Button(payment_frame, text="Add Method", font=("Arial", 14), bg="#4CAF50", fg="white",
                command=lambda: add_payment_method(new_method_var.get(), update_payment_method_label)).pack(
            pady=(10, 10), fill="x", padx=10)

        tk.Button(payment_frame, text="Back", font=("Arial", 14), bg="#FF5722", fg="white",
                command=lambda: setting_page(main_frame, user)).pack(pady=4, fill="x", padx=10)


    def get_payment_methods():
        query = """SELECT payment_method FROM users WHERE username=? """
        return execute_query(query, (user_instance,))

    def add_payment_method(method, update_label_callback):
        if method:
            try:
                query = """UPDATE users SET payment_method = ? WHERE username = ?"""
                execute_query(query, (method, user_instance))
                messagebox.showinfo("Success", "Payment method added successfully!")

                # Clear input field
                new_method_var.set("")

                # Update the payment method label
                update_label_callback()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Payment method cannot be empty!")
    # Main application loop
    
    user_id = 1  # Replace with dynamic user_id
    show_settings_page(main_frame, user_id)


# Run the application
