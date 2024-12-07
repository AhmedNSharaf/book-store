import tkinter as tk
from tkinter import Toplevel, Label, Frame
from PIL import Image, ImageTk
import sqlite3


# Colors
BG_COLOR = "#DADCDA"  # Background color
TITLE_COLOR = "#392F25"  # Title text color
TEXT_COLOR = "#563D2C"  # General text color
BUTTON_COLOR = "#80827C"  # Button color
BUTTON_TEXT_COLOR = "#DADCDA"  # Button text color

# Dummy user data
def show_profile_page(main_frame, username):
    global user
    user=username
    # Clear the main frame
    for widget in main_frame.winfo_children():
        widget.destroy()
    # Connect to the database
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    """
    # Fetch the user's current image path from the database
    cursor.execute("SELECT image_path FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    image_path = result[0] if result else None
    """
    
    
    USER_PROFILE = {
    "name": user,
    "orders": [
        {
            "order_date": "2023-12-01",
            "books": [
                {"title": "The Great Gatsby", "image": "books-piled-.png"},
                {"title": "To Kill a Mockingbird", "image": "books-piled-.pn"},
            ],
        },
        {
            "order_date": "2023-11-25",
            "books": [
                {"title": "1984", "image": "books-piled-.png"},
                {"title": "Book 4", "image": "books-piled-.png"},
            ],
        },
        {
            "order_date": "2023-11-15",
            "books": [
                {"title": "Book 5", "image": "books-piled-.png"},
            ],
        },
    ],
    "wishlist": [
        {"title": "The Catcher in the Rye", "image": "books-piled-.png"},
        {"title": "Brave New World", "image": "books-piled-.png"},
        {"title": "Pride and Prejudice", "image": "books-piled-.png"},
        {"title": "Book 4", "image": "books-piled-.png"},
        {"title": "Book 5", "image": "books-piled-.png"},
    ],
}

    # Create main window
    root = tk.Tk()
    root.title("Profile Page")
    root.geometry("600x800")
    root.configure(bg=BG_COLOR)
    root.resizable(False, False)

    # Title
    title_label = tk.Label(root, text="Profile Page", font=("Arial", 20, "bold"), fg=TITLE_COLOR, bg=BG_COLOR)
    title_label.pack(pady=10)

    # Profile Photo
    try:
        image = Image.open(USER_PROFILE["photo"])
        image = image.resize((100, 100))  # Resize image to 100x100 pixels
        photo = ImageTk.PhotoImage(image)
        photo_label = tk.Label(root, image=photo, bg=BG_COLOR)
        photo_label.image = photo  # Keep a reference to avoid garbage collection
        photo_label.pack(pady=10)
    except Exception as e:
        photo_label = tk.Label(root, text="[Photo not available]", font=("Arial", 12), fg="red", bg=BG_COLOR)
        photo_label.pack(pady=10)

    # User Details Section
    details_frame = tk.Frame(root, padx=20, pady=10, bg=BG_COLOR)
    details_frame.pack()


    # Name
    name_label = tk.Label(details_frame, text="Name:", font=("Arial", 14, "bold"), fg=TITLE_COLOR, bg=BG_COLOR)
    name_label.grid(row=0, column=0, sticky="w", pady=5)
    name_value = tk.Label(details_frame, text=USER_PROFILE["name"], font=("Arial", 14), fg=TEXT_COLOR, bg=BG_COLOR)
    name_value.grid(row=0, column=1, sticky="w", pady=5)

 
    # Function to create slider section
    def create_slider_section(parent, items, section_title, item_type="order"):
        section_label = tk.Label(parent, text=section_title, font=("Arial", 16, "bold"), fg=TITLE_COLOR, bg=BG_COLOR)
        section_label.pack(pady=10)

        slider_frame = tk.Frame(parent, padx=20, pady=10, bg=BG_COLOR)
        slider_frame.pack()

        # Current index for slider
        current_index = tk.IntVar(value=0)

        def update_items():
            # Clear the frame
            for widget in items_frame.winfo_children():
                widget.destroy()

            # Display 3 items at a time
            start_index = current_index.get()
            for item in items[start_index:start_index + 3]:  # Show 3 items at a time
                if item_type == "order":
                    item_button = tk.Button(
                        items_frame,
                        text=f"Order ({item['order_date']})",
                        font=("Arial", 12),
                        relief="flat",
                        fg=TEXT_COLOR,
                        bg=BUTTON_COLOR,
                        command=lambda o=item: show_order_details(o)
                    )
                    item_button.pack(side="left", padx=10)
                elif item_type == "wishlist":
                    item_frame = tk.Frame(items_frame, padx=10, pady=5, bg=BG_COLOR)
                    item_frame.pack(side="left", padx=10)

                    try:
                        # Load wishlist item image
                        item_image = Image.open(item["image"])
                        item_image = item_image.resize((50, 50))  # Resize to 50x50 pixels
                        item_photo = ImageTk.PhotoImage(item_image)

                        # Add item image
                        item_image_label = tk.Label(item_frame, image=item_photo, bg=BG_COLOR)
                        item_image_label.image = item_photo  # Keep a reference
                        item_image_label.pack()

                    except Exception as e:
                        print(f"Error loading wishlist item image: {e}")
                        item_image_label = tk.Label(item_frame, text="[Image not available]", font=("Arial", 10), fg="red", bg=BG_COLOR)
                        item_image_label.pack()

                    # Add item title
                    item_title_label = tk.Label(item_frame, text=item["title"], font=("Arial", 12), fg=TEXT_COLOR, bg=BG_COLOR)
                    item_title_label.pack()

        def move_left():
            if current_index.get() > 0:
                current_index.set(current_index.get() - 1)
                update_items()

        def move_right():
            if current_index.get() < len(items) - 3:  # Ensure there are at least 3 items ahead
                current_index.set(current_index.get() + 1)
                update_items()

        # Left and right arrows
        left_button = tk.Button(slider_frame, text="◀", font=("Arial", 16), command=move_left, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
        left_button.pack(side="left")

        # Items display frame
        items_frame = tk.Frame(slider_frame, bg=BG_COLOR)
        items_frame.pack(side="left", padx=10)

        # Right arrow
        right_button = tk.Button(slider_frame, text="▶", font=("Arial", 16), command=move_right, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
        right_button.pack(side="left")

        # Initial display
        update_items()


    def show_order_details(order):
        details_window = Toplevel(root)
        details_window.title("Order Details")
        details_window.geometry("400x400")
        details_window.configure(bg=BG_COLOR)

        details_label = Label(details_window, text=f"Order Date: {order['order_date']}", font=("Arial", 16, "bold"), fg=TITLE_COLOR, bg=BG_COLOR)
        details_label.pack(pady=10)

        books_frame = Frame(details_window, padx=10, pady=10, bg=BG_COLOR)
        books_frame.pack()

        for book in order["books"]:
            book_frame = Frame(books_frame, padx=10, pady=5, bg=BG_COLOR)
            book_frame.pack(fill="x")

            try:
                book_image = Image.open(book["image"])
                book_image = book_image.resize((50, 50))
                book_photo = ImageTk.PhotoImage(book_image)

                book_image_label = tk.Label(book_frame, image=book_photo, bg=BG_COLOR)
                book_image_label.image = book_photo
                book_image_label.pack(side="left", padx=5)

            except Exception as e:
                print(f"Error loading book image: {e}")
                book_image_label = tk.Label(book_frame, text="[Image not available]", font=("Arial", 10), fg="red", bg=BG_COLOR)
                book_image_label.pack(side="left", padx=5)

            book_title_label = tk.Label(book_frame, text=book["title"], font=("Arial", 12), fg=TEXT_COLOR, bg=BG_COLOR)
            book_title_label.pack(side="left", padx=10)


    # Wishlist Section
    create_slider_section(root, USER_PROFILE["wishlist"], "Wishlist", item_type="wishlist")

    # Orders Section
    create_slider_section(root, USER_PROFILE["orders"], "Orders", item_type="order")

    # Close Button
    close_button = tk.Button(root, text="Close", font=("Arial", 14), bg=TITLE_COLOR, fg=BUTTON_TEXT_COLOR, command=root.destroy)
    close_button.pack(pady=20)

    # Run the GUI
    root.mainloop()
