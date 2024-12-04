# # import tkinter as tk
# # from tkinter import ttk

# # # Sample data
# # categories = {
# #     "Fiction": ["Book 1", "Book 2", "Book 3", "Book 4", "Book 5"],
# #     "Non-Fiction": ["Book 6", "Book 7", "Book 8", "Book 9", "Book 10"],
# #     "Science": ["Book 11", "Book 12", "Book 13", "Book 14", "Book 15"],
# #     "History": ["Book 16", "Book 17", "Book 18", "Book 19", "Book 20"],
# # }

# # def open_category(category_name):
# #     category_window = tk.Toplevel(root)
# #     category_window.geometry('800x600')
# #     category_window.title(category_name)
    
# #     # Scrollable frame
# #     canvas = tk.Canvas(category_window)
# #     scrollbar = ttk.Scrollbar(category_window, orient="vertical", command=canvas.yview)
# #     scrollable_frame = ttk.Frame(canvas)

# #     scrollable_frame.bind(
# #         "<Configure>",
# #         lambda e: canvas.configure(
# #             scrollregion=canvas.bbox("all")
# #         )
# #     )
    
# #     canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
# #     canvas.configure(yscrollcommand=scrollbar.set)
    
# #     for book in categories[category_name]:
# #         book_frame = ttk.Frame(scrollable_frame, borderwidth=1, relief="solid")
# #         book_frame.pack(pady=5, padx=5, fill="x")
# #         ttk.Label(book_frame, text=book).pack(padx=10, pady=10)
    
# #     canvas.pack(side="left", fill="both", expand=True)
# #     scrollbar.pack(side="right", fill="y")

# # root = tk.Tk()
# # root.title("Bookstore Categories")
# # root.geometry('1200x800')

# # # Scrollable frame for main categories page
# # main_canvas = tk.Canvas(root)
# # main_scrollbar = ttk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
# # main_scrollable_frame = ttk.Frame(main_canvas)

# # main_scrollable_frame.bind(
# #     "<Configure>",
# #     lambda e: main_canvas.configure(
# #         scrollregion=main_canvas.bbox("all")
# #     )
# # )

# # main_canvas.create_window((0, 0), window=main_scrollable_frame, anchor="nw")
# # main_canvas.configure(yscrollcommand=main_scrollbar.set)

# # for category, books in categories.items():
# #     frame = ttk.Frame(main_scrollable_frame)
# #     frame.pack(pady=10, padx=10, fill="x", expand=True)
    
# #     # Header frame with category name and "Read More" button
# #     header_frame = ttk.Frame(frame)
# #     header_frame.pack(fill="x", padx=10)
    
# #     ttk.Label(header_frame, text=category, font=("Helvetica", 16), anchor="w").pack(side="left", padx=5)
# #     ttk.Button(header_frame, text="Read More", command=lambda c=category: open_category(c)).pack(side="right")
    
# #     # Horizontal scrollable frame for books (fixed width of 800 px)
# #     book_canvas = tk.Canvas(frame, height=180, width=800)
# #     book_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=book_canvas.xview)
# #     book_scrollable_frame = ttk.Frame(book_canvas)
    
# #     book_scrollable_frame.bind(
# #         "<Configure>",
# #         lambda e: book_canvas.configure(
# #             scrollregion=book_canvas.bbox("all")
# #         )
# #     )
    
# #     book_canvas.create_window((0, 0), window=book_scrollable_frame, anchor="nw")
# #     book_canvas.configure(xscrollcommand=book_scrollbar.set)
    
# #     for book in books:  # Display all books in the category
# #         book_frame = ttk.Frame(book_scrollable_frame, borderwidth=1, relief="solid", width=200, height=150)
# #         book_frame.pack(side="left", padx=10, pady=5)
# #         book_frame.pack_propagate(False)  # Prevent frame from resizing to fit content
# #         ttk.Label(book_frame, text=book).pack(expand=True, fill="both", padx=10, pady=10)
    
# #     # Adjust pack options to fit the defined width and expand
# #     book_canvas.pack(side="top", fill="x", expand=False)
# #     book_scrollbar.pack(side="bottom", fill="x")

# # main_canvas.pack(side="left", fill="both", expand=True)
# # main_scrollbar.pack(side="right", fill="y")

# # root.mainloop()


# import sqlite3
# from tkinter import ttk
# import tkinter as tk
# def fetch_categories_and_books():
#     conn = sqlite3.connect('user_data.db')
#     cursor = conn.cursor()
    
#     # Fetch distinct categories
#     cursor.execute("SELECT DISTINCT Category FROM Books WHERE Category IS NOT NULL")
#     categories = cursor.fetchall()

#     category_data = {}
#     for category in categories:
#         category_name = category[0]
#         cursor.execute("SELECT Title FROM Books WHERE Category = ?", (category_name,))
#         books = cursor.fetchall()
#         category_data[category_name] = [book[0] for book in books]
    
#     conn.close()
#     return category_data
# # Fetch categories and books dynamically
# categories = fetch_categories_and_books()

# def open_category(category_name):
#     category_window = tk.Toplevel(root)
#     category_window.geometry('800x600')
#     category_window.title(category_name)
    
#     canvas = tk.Canvas(category_window)
#     scrollbar = ttk.Scrollbar(category_window, orient="vertical", command=canvas.yview)
#     scrollable_frame = ttk.Frame(canvas)

#     scrollable_frame.bind(
#         "<Configure>",
#         lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
#     )
    
#     canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
#     canvas.configure(yscrollcommand=scrollbar.set)
    
#     for book in categories[category_name]:
#         book_frame = ttk.Frame(scrollable_frame, borderwidth=1, relief="solid")
#         book_frame.pack(pady=5, padx=5, fill="x")
#         ttk.Label(book_frame, text=book).pack(padx=10, pady=10)
    
#     canvas.pack(side="left", fill="both", expand=True)
#     scrollbar.pack(side="right", fill="y")

# root = tk.Tk()
# root.title("Bookstore Categories")
# root.geometry('1200x800')

# main_canvas = tk.Canvas(root)
# main_scrollbar = ttk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
# main_scrollable_frame = ttk.Frame(main_canvas)

# main_scrollable_frame.bind(
#     "<Configure>",
#     lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
# )

# main_canvas.create_window((0, 0), window=main_scrollable_frame, anchor="nw")
# main_canvas.configure(yscrollcommand=main_scrollbar.set)

# for category, books in categories.items():
#     frame = ttk.Frame(main_scrollable_frame)
#     frame.pack(pady=10, padx=10, fill="x", expand=True)
    
#     header_frame = ttk.Frame(frame)
#     header_frame.pack(fill="x", padx=10)
    
#     ttk.Label(header_frame, text=category, font=("Helvetica", 16), anchor="w").pack(side="left", padx=5)
#     ttk.Button(header_frame, text="Read More", command=lambda c=category: open_category(c)).pack(side="right")
    
#     book_canvas = tk.Canvas(frame, height=180, width=800)
#     book_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=book_canvas.xview)
#     book_scrollable_frame = ttk.Frame(book_canvas)
    
#     book_scrollable_frame.bind(
#         "<Configure>",
#         lambda e: book_canvas.configure(scrollregion=book_canvas.bbox("all"))
#     )
    
#     book_canvas.create_window((0, 0), window=book_scrollable_frame, anchor="nw")
#     book_canvas.configure(xscrollcommand=book_scrollbar.set)
    
#     for book in books:
#         book_frame = ttk.Frame(book_scrollable_frame, borderwidth=1, relief="solid", width=200, height=150)
#         book_frame.pack(side="left", padx=10, pady=5)
#         book_frame.pack_propagate(False)
#         ttk.Label(book_frame, text=book).pack(expand=True, fill="both", padx=10, pady=10)
    
#     book_canvas.pack(side="top", fill="x", expand=False)
#     book_scrollbar.pack(side="bottom", fill="x")

# main_canvas.pack(side="left", fill="both", expand=True)
# main_scrollbar.pack(side="right", fill="y")

# root.mainloop()
