import sqlite3
import tkinter as tk
from tkinter import ttk
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
    user_balance = tk.DoubleVar(value=get_balance(username))  # Fetch balance using the get_balance function

    tk.Label(profile_frame, text=username, font=("Arial", 16, "bold"), bg="#FAF9F6").pack(pady=5)
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

    # Function to display orders
    def display_orders():
        cursor.execute("SELECT Order_ID, Order_Date, Total_Cost FROM Orders WHERE user_id = (SELECT id FROM users WHERE username = ?)", (username,))
        orders = cursor.fetchall()

        if not orders:
            messagebox.showinfo("No Orders", "You have not placed any orders yet.")
            return

        # Dropdown to select an order
        order_selection_frame = tk.Frame(profile_frame, bg="#FAF9F6")
        order_selection_frame.pack(pady=10)

        tk.Label(order_selection_frame, text="Your Orders:", font=("Arial", 12), bg="#FAF9F6").pack(side="left", padx=5)

        order_var = tk.StringVar()
        order_dropdown = ttk.Combobox(order_selection_frame, textvariable=order_var, state="readonly", width=50)
        order_dropdown['values'] = [f"Order ID: {order[0]} | Date: {order[1]} | Total: ${order[2]:.2f}" for order in orders]
        order_dropdown.pack(side="left", padx=5)

        def view_order_details():
            selected_order = order_var.get()
            if not selected_order:
                messagebox.showwarning("No Selection", "Please select an order to view details.")
                return

            selected_order_id = int(selected_order.split()[2])  # Extract the Order_ID
            cursor.execute("SELECT * FROM Orders WHERE Order_ID = ?", (selected_order_id,))
            order_details = cursor.fetchone()

            if order_details:
                details_message = "\n".join([f"{col}: {val}" for col, val in zip([desc[0] for desc in cursor.description], order_details)])
                messagebox.showinfo("Order Details", details_message)

        view_details_button = tk.Button(order_selection_frame, text="View Details", font=("Arial", 12), bg="#FFC107", fg="black", command=view_order_details)
        view_details_button.pack(side="left", padx=5)

    # Display Orders Button
    display_orders_button = tk.Button(
        profile_frame, text="Display My Orders", font=("Arial", 12), bg="#673AB7", fg="white", command=display_orders
    )
    display_orders_button.pack(pady=20)

    # Close database connection
    # conn.close()
