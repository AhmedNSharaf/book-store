import sqlite3
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import simpledialog, messagebox

from get_balance import get_balance
def show_profile_page(main_frame, username="a"):
    # Clear the main frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Profile Page Content
    profile_frame = tk.Frame(main_frame, bg="#FAF9F6")
    profile_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # User Image
    try:
        user_img = Image.open("WhatsApp Image 2024-07-03 at 19.56.48_ae64950a.jpg").resize((100, 100))
        user_img_tk = ImageTk.PhotoImage(user_img)
        user_img_label = tk.Label(profile_frame, image=user_img_tk, bg="#FAF9F6")
        user_img_label.image = user_img_tk  # Keep a reference to avoid garbage collection
        user_img_label.pack(pady=10)
    except Exception as e:
        tk.Label(profile_frame, text="User Image Not Found", font=("Arial", 12), bg="#FAF9F6", fg="red").pack(pady=10)



    # User Info
    user_name = username  # Example username passed to the function
    user_id = "12345"  # Example user ID
    user_balance = tk.DoubleVar(value=get_balance(username))  # Fetch balance using the get_balance function

    tk.Label(profile_frame, text=user_name, font=("Arial", 16, "bold"), bg="#FAF9F6").pack(pady=5)
    tk.Label(profile_frame, text=f"User ID: {user_id}", font=("Arial", 12), bg="#FAF9F6", fg="gray").pack(pady=5)
    balance_label = tk.Label(profile_frame, text=f"Balance: {user_balance.get()}$", font=("Arial", 12, "bold"), bg="#FAF9F6")
    balance_label.pack(pady=10)

    # Function to add balance
    def add_balance():
        try:
            amount = simpledialog.askfloat("Add Balance", "Enter the amount to add:", minvalue=0)
            if amount is not None:
                new_balance = user_balance.get() + amount
                user_balance.set(new_balance)
                balance_label.config(text=f"Balance: {user_balance.get()}$")
                messagebox.showinfo("Success", f"{amount}$ has been added to your balance.")

                # Update the database
                conn = sqlite3.connect('user_data.db')
                cursor = conn.cursor()
                cursor.execute('UPDATE users SET balance = ? WHERE username = ?', (new_balance, username))
                conn.commit()
                conn.close()
            else:
                messagebox.showinfo("Cancelled", "No amount was added.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Add Balance Button
    add_balance_button = tk.Button(profile_frame, text="Add Balance", font=("Arial", 12), bg="#4CAF50", fg="white", command=add_balance)
    add_balance_button.pack(pady=20)
