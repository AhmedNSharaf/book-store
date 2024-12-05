import sqlite3
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import simpledialog, messagebox, filedialog
import os
from get_balance import get_balance

def show_profile_page(main_frame, username):
    # Clear the main frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Connect to the database
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Fetch the user's current image path from the database
    cursor.execute("SELECT image_path FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    image_path = result[0] if result else None

    # Profile Page Content
    profile_frame = tk.Frame(main_frame, bg="#FAF9F6")
    profile_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # User Image
    def update_image():
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")]
        )
        if file_path:
            # Save image to a designated directory
            try:
                user_dir = "user_images"
                os.makedirs(user_dir, exist_ok=True)
                user_image_path = os.path.join(user_dir, f"{username}_profile.jpg")
                with open(file_path, "rb") as src, open(user_image_path, "wb") as dst:
                    dst.write(src.read())

                # Update the database with the new image path
                cursor.execute("UPDATE users SET image_path = ? WHERE username = ?", (user_image_path, username))
                conn.commit()

                # Update the displayed image
                display_image(user_image_path)
                messagebox.showinfo("Success", "Profile picture updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not update image: {e}")

    def display_image(img_path):
        try:
            user_img = Image.open(img_path).resize((100, 100))
            user_img_tk = ImageTk.PhotoImage(user_img)
            user_img_label.config(image=user_img_tk)
            user_img_label.image = user_img_tk  # Keep a reference to avoid garbage collection
        except Exception as e:
            user_img_label.config(text="No Image Found", image="", fg="red")

    user_img_label = tk.Label(profile_frame, bg="#FAF9F6", text="No Image Found", fg="gray")
    user_img_label.pack(pady=10)

    # Display the current image if it exists
    if image_path:
        display_image(image_path)

    update_image_button = tk.Button(
        profile_frame, text="Change Profile Picture", font=("Arial", 12), bg="#007BFF", fg="white", command=update_image
    )
    update_image_button.pack(pady=10)

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
                cursor.execute('UPDATE users SET balance = ? WHERE username = ?', (new_balance, username))
                conn.commit()
            else:
                messagebox.showinfo("Cancelled", "No amount was added.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Add Balance Button
    add_balance_button = tk.Button(
        profile_frame, text="Add Balance", font=("Arial", 12), bg="#4CAF50", fg="white", command=add_balance
    )
    add_balance_button.pack(pady=20)

    # Close database connection
