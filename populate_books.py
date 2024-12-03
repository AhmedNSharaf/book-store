import tkinter as tk
from PIL import Image, ImageTk
def populate_books(container, books, row_start, section_title):
    title_label = tk.Label(container, text=section_title, font=("Arial", 18, "bold"), bg="#FAF9F6")
    title_label.grid(row=row_start, column=0, sticky="w", padx=20, pady=10)
    
    book_frame = tk.Frame(container, bg="#FAF9F6")
    book_frame.grid(row=row_start + 1, column=0, sticky="w", padx=20, pady=5)
    
    for idx, book in enumerate(books):
        frame = tk.Frame(book_frame, bg="#FFFFFF", relief="raised", padx=10, pady=10)
        frame.grid(row=0, column=idx, padx=10, pady=5)
        
        # Book image
        image = Image.open(book["image"]).resize((100, 150))
        img = ImageTk.PhotoImage(image)
        img_label = tk.Label(frame, image=img, bg="#FFFFFF")
        img_label.image = img
        img_label.pack()
        
        # Book title
        tk.Label(frame, text=book["title"], font=("Arial", 12, "bold"), bg="#FFFFFF").pack(pady=5)
        # Author
        tk.Label(frame, text=f'by {book["author"]}', font=("Arial", 10), fg="gray", bg="#FFFFFF").pack()
        # Rating
        tk.Label(frame, text="★" * book["rating"], font=("Arial", 10), fg="gold", bg="#FFFFFF").pack()
