import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
from center_window import center_window

DATABASE = 'user_data.db'
image_cache = {}  # Cache to store loaded images

# A stop event for threads
stop_event = threading.Event()

def show_category_page(main_area):
    def fetch_image(image_path, label):
        """
        Load and display an image asynchronously.
        """
        def load_image():
            if image_path not in image_cache:
                try:
                    # Check if the stop event is set, stop loading the image
                    if stop_event.is_set():
                        return
                    
                    img = Image.open(image_path)
                    img = img.resize((90, 120))  # Resize to fit the card
                    image_cache[image_path] = ImageTk.PhotoImage(img)
                except Exception as e:
                    print(f"Error loading image {image_path}: {e}")
                    return
            label.config(image=image_cache[image_path])
            label.image = image_cache[image_path]  # Keep a reference to prevent garbage collection

        threading.Thread(target=load_image, daemon=True).start()

    def view_book_details(book_id):
        """
        Display detailed information about a selected book.
        """
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT ISBN, Title, Author, Category, Publication, Price, image_path FROM Books WHERE BookID = ?", (book_id,))
        book_details = cursor.fetchone()
        conn.close()

        if book_details:
            # Display book details in a new window
            global details_window
            details_window = tk.Toplevel(main_area)
            details_window.title(f"Book Details - {book_details[1]}")

            if book_details[6]:
                img = Image.open(book_details[6])
                img = img.resize((150, 200))  # Resize to fit the label
                img_tk = ImageTk.PhotoImage(img)
                img_label = tk.Label(details_window, image=img_tk)
                img_label.image = img_tk  # Keep a reference to the image
                img_label.pack(pady=10)

            tk.Label(details_window, text=f"Title: {book_details[1]}", font=("Arial", 12)).pack(pady=5)
            tk.Label(details_window, text=f"Author: {book_details[2]}", font=("Arial", 12)).pack(pady=5)
            tk.Label(details_window, text=f"Category: {book_details[3]}", font=("Arial", 12)).pack(pady=5)
            tk.Label(details_window, text=f"Publication: {book_details[4]}", font=("Arial", 12)).pack(pady=5)
            tk.Label(details_window, text=f"Price: ${book_details[5]:.2f}", fg="green", font=("Arial", 12)).pack(pady=5)

            # Add a Close button
            close_button = tk.Button(details_window, text="Close", command=details_window.destroy, bg="red", fg="white", font=("Arial", 10, "bold"))
            close_button.pack(pady=10)

            center_window(details_window, 500, 500)
        else:
            messagebox.showerror("Error", "Could not retrieve book details.")

    def on_mouse_wheel(event, canvas):
        """
        Scroll the canvas vertically using the mouse wheel.
        """
        canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def on_horizontal_scroll(event, canvas):
        """
        Scroll the canvas horizontally using the mouse wheel with Shift key pressed.
        """
        canvas.xview_scroll(-1 * int(event.delta / 120), "units")

    def display_books_by_category():
        """
        Fetch and display books grouped by categories.
        """
        # Clear previous widgets in the main area
        for widget in main_area.winfo_children():
            widget.destroy()

        # Create a Canvas for vertical scrolling
        canvas = tk.Canvas(main_area)
        canvas.pack(side="left", fill="both", expand=True)

        # Add a vertical scrollbar for the canvas
        scrollbar = tk.Scrollbar(main_area, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # Configure the canvas to work with the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Enable vertical scrolling with the mouse wheel
        canvas.bind_all("<MouseWheel>", lambda event: on_mouse_wheel(event, canvas))

        # Create a Frame inside the Canvas to hold the content
        content_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor="nw", width=1300)

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT Category FROM Books")
        categories = cursor.fetchall()
        conn.close()

        if not categories:
            messagebox.showinfo("No Categories", "No categories found in the database.")
            return

        for category in categories:
            category_name = category[0]

            # Create a frame for each category
            category_frame = tk.Frame(content_frame, bd=1, relief="solid", padx=10, pady=10)
            category_frame.pack(fill="x", pady=5)

            category_label = tk.Label(category_frame, text=category_name, font=("Arial", 14, "bold"))
            category_label.pack(pady=5)

            # Create a Canvas for horizontal scrolling inside each category
            category_canvas = tk.Canvas(category_frame)
            category_canvas.pack(side="left", fill="both", expand=True)

            # Add a horizontal scrollbar for the category
            category_scrollbar = tk.Scrollbar(category_frame, orient="horizontal", command=category_canvas.xview)
            category_scrollbar.pack(side="bottom", fill="x")

            # Configure the category canvas to work with the horizontal scrollbar
            category_canvas.configure(xscrollcommand=category_scrollbar.set)
            
            # Enable horizontal scrolling with Shift + Mouse Wheel
            category_canvas.bind("<Shift-MouseWheel>", lambda event, c=category_canvas: on_horizontal_scroll(event, c))

            # Create a Frame inside the category canvas to hold the books
            books_frame = tk.Frame(category_canvas)
            category_canvas.create_window((0, 0), window=books_frame, anchor="nw")

            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute("SELECT BookID, Title, Author, Price, image_path FROM Books WHERE Category = ?", (category_name,))
            books = cursor.fetchall()
            conn.close()

            if not books:
                tk.Label(category_frame, text="No books available in this category.", font=("Arial", 12), fg="gray").pack(pady=5)
                continue

            for book in books:
                book_id, book_title, book_author, book_price, image_path = book

                book_card = tk.Frame(books_frame, bd=2, relief="solid", padx=10, pady=3, width=200, height=250)
                book_card.pack(side="left", padx=10, pady=10)

                placeholder = tk.Label(book_card, text="Loading...", font=("Arial", 9))
                placeholder.pack(pady=3)

                if image_path:
                    fetch_image(image_path, placeholder)

                book_info_frame = tk.Frame(book_card)
                book_info_frame.pack(pady=5)

                tk.Label(book_info_frame, text=f"Title: {book_title}", font=("Arial", 10, "bold")).pack(pady=1)
                tk.Label(book_info_frame, text=f"Author: {book_author}", font=("Arial", 9)).pack(pady=1)
                tk.Label(book_info_frame, text=f"Price: ${book_price:.2f}", font=("Arial", 9, "bold")).pack(pady=1)

                view_button = tk.Button(book_card, text="View Details", command=lambda book_id=book_id: view_book_details(book_id))
                view_button.pack(pady=2)

            books_frame.update_idletasks()
            category_canvas.config(scrollregion=category_canvas.bbox("all"))

        # Reinitialize the scroll region for the main canvas
        content_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    # Call the function to display categories
    display_books_by_category()

    # Stop any running threads when the main area is destroyed
    def on_close():
        stop_event.set()  # Signal threads to stop
        main_area.destroy()

    main_area.protocol("WM_DELETE_WINDOW", on_close)
