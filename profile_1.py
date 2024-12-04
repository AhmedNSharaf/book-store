import tkinter as tk
from PIL import Image, ImageTk  # For handling profile pictures

# Dummy user data
USER_PROFILE = {
    "name": "John Doe",
    "email": "johndoe@example.com",
    "photo": "profile.jpg",  # Replace with the path to your image
    "purchased_books": ["The Great Gatsby", "To Kill a Mockingbird", "1984"],
    "wishlist": ["The Catcher in the Rye", "Brave New World", "Pride and Prejudice"]
}

# Create main window
root = tk.Tk()
root.title("Profile Page")
root.geometry("600x600")
root.resizable(False, False)

# Title
title_label = tk.Label(root, text="Profile Page", font=("Arial", 20, "bold"))
title_label.pack(pady=10)

# Profile Photo
try:
    image = Image.open(USER_PROFILE["photo"])
    image = image.resize((100, 100))  # Resize image to 100x100 pixels
    photo = ImageTk.PhotoImage(image)
    photo_label = tk.Label(root, image=photo)
    photo_label.image = photo  # Keep a reference to avoid garbage collection
    photo_label.pack(pady=10)
except Exception as e:
    photo_label = tk.Label(root, text="[Photo not available]", font=("Arial", 12), fg="red")
    photo_label.pack(pady=10)

# User Details Section
details_frame = tk.Frame(root, padx=20, pady=10)
details_frame.pack()

# Name
name_label = tk.Label(details_frame, text="Name:", font=("Arial", 14, "bold"))
name_label.grid(row=0, column=0, sticky="w", pady=5)
name_value = tk.Label(details_frame, text=USER_PROFILE["name"], font=("Arial", 14))
name_value.grid(row=0, column=1, sticky="w", pady=5)

# Email
email_label = tk.Label(details_frame, text="Email:", font=("Arial", 14, "bold"))
email_label.grid(row=1, column=0, sticky="w", pady=5)
email_value = tk.Label(details_frame, text=USER_PROFILE["email"], font=("Arial", 14))
email_value.grid(row=1, column=1, sticky="w", pady=5)

# Purchased Books Section
books_label = tk.Label(root, text="Purchased Books:", font=("Arial", 16, "bold"))
books_label.pack(pady=10)

books_frame = tk.Frame(root, padx=20)
books_frame.pack()

for book in USER_PROFILE["purchased_books"]:
    tk.Label(books_frame, text=f"• {book}", font=("Arial", 12)).pack(anchor="w")

# Wishlist Section
wishlist_label = tk.Label(root, text="Wishlist:", font=("Arial", 16, "bold"))
wishlist_label.pack(pady=10)

wishlist_frame = tk.Frame(root, padx=20)
wishlist_frame.pack()

for book in USER_PROFILE["wishlist"]:
    tk.Label(wishlist_frame, text=f"• {book}", font=("Arial", 12)).pack(anchor="w")

# Close Button
close_button = tk.Button(root, text="Close", font=("Arial", 14), bg="red", fg="white", command=root.destroy)
close_button.pack(pady=20)

# Run the GUI
root.mainloop()
