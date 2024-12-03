# import tkinter as tk
# from tkinter import ttk
# from PIL import Image, ImageTk

# def create_home_page(root, main_frame, books):
#     # Clear the main frame
#     for widget in main_frame.winfo_children():
#         widget.destroy()

#     # Populate books
#     for idx, book in enumerate(books):
#         frame = tk.Frame(main_frame, bg="#FFFFFF", padx=10, pady=10)
#         frame.grid(row=0, column=idx, padx=20, pady=20)

#         # Book image
#         image = Image.open(book["image"]).resize((100, 150))
#         img = ImageTk.PhotoImage(image)
#         img_label = tk.Label(frame, image=img, bg="#FFFFFF")
#         img_label.image = img
#         img_label.pack()

#         # Book title
#         tk.Label(frame, text=book["title"], font=("Arial", 12, "bold"), bg="#FFFFFF").pack(pady=5)
        
#         # Author
#         tk.Label(frame, text=f'by {book["author"]}', font=("Arial", 10), bg="#FFFFFF", fg="gray").pack()

#         # Bind click event to open details page
#         frame.bind("<Button-1>", lambda e, b=book: show_book_details(root, main_frame, b))
#         img_label.bind("<Button-1>", lambda e, b=book: show_book_details(root, main_frame, b))

# def show_book_details(root, main_frame, book):
#     # Clear the main frame
#     for widget in main_frame.winfo_children():
#         widget.destroy()

#     # Book image
#     image = Image.open(book["image"]).resize((200, 300))
#     img = ImageTk.PhotoImage(image)
#     img_label = tk.Label(main_frame, image=img, bg="#FAF9F6")
#     img_label.image = img
#     img_label.pack(pady=20)

#     # Book title
#     tk.Label(main_frame, text=book["title"], font=("Arial", 18, "bold"), bg="#FAF9F6").pack(pady=10)

#     # Author
#     tk.Label(main_frame, text=f"Author: {book['author']}", font=("Arial", 14), bg="#FAF9F6").pack(pady=5)

#     # Rating
#     tk.Label(main_frame, text="Rating: " + "★" * book["rating"], font=("Arial", 12), fg="gold", bg="#FAF9F6").pack(pady=5)

#     # Back Button
#     back_button = tk.Button(main_frame, text="← Back to Home", font=("Arial", 12), bg="#FCE6C9", command=lambda: create_home_page(root, main_frame, books))
#     back_button.pack(pady=30)

# if __name__ == "__main__":
#     # Root window
#     root = tk.Tk()
#     root.title("Book Store App")
#     root.geometry("800x600")
#     root.configure(bg="#FAF9F6")

#     # Main frame for dynamic content
#     main_frame = tk.Frame(root, bg="#FAF9F6")
#     main_frame.pack(fill="both", expand=True)

#     # Sample Book Data
#     books = [
#         {"title": "It Starts with Us", "author": "Colleen Hoover", "rating": 4, "image": "books-piled-.png"},
#         {"title": "Fairy Tale", "author": "Stephen King", "rating": 5, "image": "books-piled-.png"},
#         {"title": "The Thursday Murder Club", "author": "Richard Osman", "rating": 4, "image": "books-piled-.png"},
#         {"title": "Normal People", "author": "Sally Rooney", "rating": 3, "image": "books-piled-.png"},
#         {"title": "Atomic Habits", "author": "James Clear", "rating": 5, "image": "books-piled-.png"},
#     ]

#     # Initialize with the home page
#     create_home_page(root, main_frame, books)

#     root.mainloop()




import tkinter as tk
from PIL import Image, ImageTk

def create_sidebar(root, main_frame, books):
    """Create a sidebar with navigation buttons."""
    sidebar = tk.Frame(root, bg="#FCE6C9", width=200)
    sidebar.pack(side="left", fill="y")

    # User Profile Section
    user_img = Image.open("WhatsApp Image 2024-07-03 at 19.56.48_ae64950a.jpg").resize((50, 50))
    user_img_tk = ImageTk.PhotoImage(user_img)
    user_img_label = tk.Label(sidebar, image=user_img_tk, bg="#FCE6C9")
    user_img_label.image = user_img_tk
    user_img_label.pack(pady=20)

    tk.Label(sidebar, text="Youmna Mohamed", font=("Arial", 14, "bold"), bg="#FCE6C9").pack()
    
    # Navigation Buttons
    buttons = ["Home", "Categories", "Saved", "Recommendations", "Settings", "Profile"]
    for btn_text in buttons:
        btn = tk.Button(
            sidebar, text=btn_text, font=("Arial", 12),
            bg="#FCE6C9", relief="flat", anchor="w", padx=10,
            command=lambda text=btn_text: handle_nav(text, root, main_frame, books)
        )
        btn.pack(fill="x", pady=5)
    
    tk.Button(sidebar, text="LOG OUT", font=("Arial", 12), bg="black", fg="white", relief="flat",
              command=log_out).pack(pady=20)
    
def log_out():
    root.destroy()  # Close the main app window
    
    # Import registration screen here to avoid circular import at the top level
    from registration import create_sign_in_window
    create_sign_in_window()  # Open the registration screen

def handle_nav(option, root, main_frame, books):
    """Handle sidebar navigation clicks."""
    if option == "Home":
        create_home_page(root, main_frame, books)
    else:
        for widget in main_frame.winfo_children():
            widget.destroy()
        tk.Label(main_frame, text=f"{option} Page", font=("Arial", 18, "bold"), bg="#FAF9F6").pack(pady=20)

def create_home_page(root, main_frame, books):
    """Create the home page with a grid of books."""
    for widget in main_frame.winfo_children():
        widget.destroy()

    title_label = tk.Label(main_frame, text="Popular Books", font=("Arial", 18, "bold"), bg="#FAF9F6")
    title_label.grid(row=0, column=0, pady=10, padx=10)

    for idx, book in enumerate(books):
        frame = tk.Frame(main_frame, bg="#FFFFFF", padx=10, pady=10)
        frame.grid(row=1 + idx // 3, column=idx % 3, padx=20, pady=20)

        image = Image.open(book["image"]).resize((100, 150))
        img = ImageTk.PhotoImage(image)
        img_label = tk.Label(frame, image=img, bg="#FFFFFF")
        img_label.image = img
        img_label.pack()

        tk.Label(frame, text=book["title"], font=("Arial", 12, "bold"), bg="#FFFFFF").pack(pady=5)
        tk.Label(frame, text=f'by {book["author"]}', font=("Arial", 10), bg="#FFFFFF", fg="gray").pack()

        frame.bind("<Button-1>", lambda e, b=book: show_book_details(root, main_frame, b))
        img_label.bind("<Button-1>", lambda e, b=book: show_book_details(root, main_frame, b))

def show_book_details(root, main_frame, book):
    """Show a detailed view of the selected book."""
    for widget in main_frame.winfo_children():
        widget.destroy()

    image = Image.open(book["image"]).resize((200, 300))
    img = ImageTk.PhotoImage(image)
    img_label = tk.Label(main_frame, image=img, bg="#FAF9F6")
    img_label.image = img
    img_label.pack(pady=20)

    tk.Label(main_frame, text=book["title"], font=("Arial", 18, "bold"), bg="#FAF9F6").pack(pady=10)
    tk.Label(main_frame, text=f"Author: {book['author']}", font=("Arial", 14), bg="#FAF9F6").pack(pady=5)
    tk.Label(main_frame, text="Rating: " + "★" * book["rating"], font=("Arial", 12), fg="gold", bg="#FAF9F6").pack(pady=5)

    back_button = tk.Button(main_frame, text="← Back to Home", font=("Arial", 12), bg="#FCE6C9",
                            command=lambda: create_home_page(root, main_frame, books))
    back_button.pack(pady=30)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Book Store App")
    root.geometry("1000x600")
    root.configure(bg="#FAF9F6")

    main_frame = tk.Frame(root, bg="#FAF9F6")
    main_frame.pack(side="right", fill="both", expand=True)

    books = [
        {"title": "It Starts with Us", "author": "Colleen Hoover", "rating": 4, "image": "books-piled-.png"},
        {"title": "Fairy Tale", "author": "Stephen King", "rating": 5, "image": "books-piled-.png"},
        {"title": "The Thursday Murder Club", "author": "Richard Osman", "rating": 4, "image": "books-piled-.png"},
        {"title": "Normal People", "author": "Sally Rooney", "rating": 3, "image": "books-piled-.png"},
        {"title": "Atomic Habits", "author": "James Clear", "rating": 5, "image": "books-piled-.png"},
    ]

    create_sidebar(root, main_frame, books)
    create_home_page(root, main_frame, books)
    root.mainloop()










