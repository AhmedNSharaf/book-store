import tkinter as tk
from populate_books import populate_books
def show_home_page(main_frame):
    # Clear the main frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Recreate the main content
    popular_books = [
        {"title": "It Starts with Us", "author": "Colleen Hoover", "rating": 4, "image": "books-piled-.png"},
        {"title": "Fairy Tale", "author": "Stephen King", "rating": 5, "image": "books-piled-.png"},
        {"title": "The Thursday Murder Club", "author": "Richard Osman", "rating": 4, "image": "books-piled-.png"},
        {"title": "Normal People", "author": "Sally Rooney", "rating": 3, "image": "books-piled-.png"},
        {"title": "Atomic Habits", "author": "James Clear", "rating": 5, "image": "books-piled-.png"},
    ]
    
    recommended_books = [
        {"title": "Book A", "author": "Author A", "rating": 5, "image": "books-piled-.png"},
        {"title": "Book B", "author": "Author B", "rating": 4, "image": "books-piled-.png"},
    ]

    content_frame = tk.Frame(main_frame, bg="#FAF9F6")
    content_frame.pack(fill="both", expand=True)
    populate_books(content_frame, popular_books, row_start=0, section_title="Popular")
    populate_books(content_frame, recommended_books, row_start=3, section_title="We Recommend")
