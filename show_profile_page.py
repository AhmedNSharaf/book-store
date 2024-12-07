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
    # Function to display orders in a scrollable frame
    def display_orders():
        # Fetch user orders
        cursor.execute("SELECT Order_ID, Order_Date, Delivery_Date,Total_Cost FROM Orders WHERE user_id = (SELECT id FROM users WHERE username = ?)", (username,))
        orders = cursor.fetchall()

        if not orders:
            tk.Label(profile_frame, text="You have not placed any orders yet.", font=("Arial", 12), bg="#FAF9F6", fg="gray").pack(pady=10)
            return

        # Create a frame for the scrollable content
        orders_frame = tk.Frame(profile_frame, bg="#FAF9F6")
        orders_frame.pack(fill="both", expand=True, pady=10)

        # Create a canvas for horizontal scrolling
        canvas = tk.Canvas(orders_frame, bg="#FAF9F6", highlightthickness=0)
        canvas.pack(side="top", fill="both", expand=True)

        # Create a frame inside the canvas to hold the cards
        scrollable_frame = tk.Frame(canvas, bg="#FAF9F6")

        # Bind the canvas to the scrollable frame
        scrollable_frame_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Populate the scrollable frame with order cards
        for index, order in enumerate(orders, start=1):
            order_id, order_date,delivery_date, total_cost = order

            # Create an individual order card
            order_card = tk.Frame(scrollable_frame, bg="#FFFFFF", bd=1, relief="solid", padx=10, pady=10, width=200, height=150)
            order_card.grid(row=0, column=index - 1, padx=10)

            # Display order summary in the card
            tk.Label(order_card, text=f"Order Date: {order_date}", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(anchor="w")
            tk.Label(order_card, text=f"Delivery Date: {delivery_date}", font=("Arial", 10), bg="#FFFFFF").pack(anchor="w")
            tk.Label(order_card, text=f"Total: ${total_cost:.2f}", font=("Arial", 10, "bold"), bg="#FFFFFF", fg="#4CAF50").pack(anchor="w")

            # Add a button to view order details
            view_details_button = tk.Button(
                order_card, text="View Details", font=("Arial", 9), bg="#007BFF", fg="white",
                command=lambda order_id=order_id: view_order_details(order_id)
            )
            view_details_button.pack(pady=5)

        # Configure the canvas scroll region dynamically
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", configure_scroll_region)

        # Handle resizing of the scrollable frame dynamically
        def resize_canvas(event):
            canvas.itemconfig(scrollable_frame_id, height=event.height)

        canvas.bind("<Configure>", resize_canvas)

        # Add a horizontal scrollbar directly below the canvas
        scrollbar = tk.Scrollbar(orders_frame, orient="horizontal", command=canvas.xview)
        scrollbar.pack(side="bottom", fill="x")

        # Connect canvas and scrollbar
        canvas.configure(xscrollcommand=scrollbar.set)

    # Function to display order details in a pop-up
    def view_order_details(order_id):
        cursor.execute("SELECT * FROM Orders WHERE Order_ID = ?", (order_id,))
        order_details = cursor.fetchone()

        if order_details:
            # Create a message displaying order details
            details_message = "\n".join([f"{col}: {val}" for col, val in zip([desc[0] for desc in cursor.description], order_details)])
            messagebox.showinfo("Order Details", details_message)
        else:
            messagebox.showerror("Error", "Order details could not be retrieved.")

    # Display Orders Button
    display_orders_button = tk.Button(
        profile_frame, text="Display My Orders", font=("Arial", 12), bg="#673AB7", fg="white", command=display_orders
    )
    display_orders_button.pack(pady=20)

