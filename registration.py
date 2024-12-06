import os
import tkinter as tk
from PIL import Image, ImageTk

from setting_esraa import setting_page

#from cart_page import show_cart_page
from cart_page import *

from create_management_page_original import create_management_page

# Global variable to track the current window
current_window = None

# Function to center the window
from center_window import center_window

# Function to create the SQLite database and table
from create_database import create_database

# Assuming `get_balance` is already defined
from get_balance import get_balance

# Function to check if a user already exists in the database
from user_exists import user_exists

# Function to show profile page
from show_profile_page import show_profile_page

# Function to insert user data into the database
from insert_user import insert_user

# Function to check user credentials during sign-in
from check_user_credentials import check_user_credentials,check_admin_credentials

from show_home_page import show_home_page
from populate_books import populate_books

# Function to navigate to the main app
def open_main_app():
    global current_window
    
    try:
        if current_window == 'sign_in':
            sign_in_window.destroy()  # Destroy Sign In window
        elif current_window == 'sign_up':
            sign_up_window.destroy()  # Destroy Sign Up window
        elif current_window == 'admin_sign_in':
            admin_sign_in_window.destroy()  # Destroy Admin Sign In window
        elif current_window == 'user_sign_in':
            user_sign_in_window.destroy()  # Destroy User Sign In window
        
        create_main_app()  # Open the main app
    except Exception as e:
        print(f"Error in open_main_app: {e}")

# Function to handle Admin Sign In
def admin_sign_in():
    global current_window
    try:
        sign_in_window.destroy()  # Close the previous window
        global admin_sign_in_window
        admin_sign_in_window = tk.Tk()
        admin_sign_in_window.title("Admin Sign In")
        admin_sign_in_window.configure(bg="#FAF9F6")

        tk.Label(admin_sign_in_window, text="Admin Sign In", font=("Arial", 18, "bold"), bg="#FAF9F6").pack(pady=20)

        tk.Label(admin_sign_in_window, text="Username", font=("Arial", 12), bg="#FAF9F6").pack(pady=5)
        admin_username_entry = tk.Entry(admin_sign_in_window, font=("Arial", 12), width=30)
        admin_username_entry.pack(pady=5)

        tk.Label(admin_sign_in_window, text="Password", font=("Arial", 12), bg="#FAF9F6").pack(pady=5)
        admin_password_entry = tk.Entry(admin_sign_in_window, font=("Arial", 12), width=30, show="*")
        admin_password_entry.pack(pady=5)

        tk.Label(admin_sign_in_window, text="Admin Key", font=("Arial", 12), bg="#FAF9F6").pack(pady=5)
        admin_key_entry = tk.Entry(admin_sign_in_window, font=("Arial", 12), width=30)
        admin_key_entry.pack(pady=5)

        def handle_admin_sign_in():
            global user
            username = admin_username_entry.get()
            user = username
            password = admin_password_entry.get()
            admin_key = admin_key_entry.get()

            if username=='a'and password=='a'and admin_key=='a':
                print("Admin Sign In successful")
                admin_sign_in_window.destroy()
                create_management_page()
            else:
                print("Invalid username or password. Try again.")
                messagebox.showerror("error","Invalid credentials. Try again.")

        sign_in_btn = tk.Button(admin_sign_in_window, text="Sign In", font=("Arial", 12), bg="#FF5722", fg="white", width=20, command=handle_admin_sign_in)
        sign_in_btn.pack(pady=20)

        current_window = 'admin_sign_in'

        # Center the window
        center_window(admin_sign_in_window, 400, 400)

        admin_sign_in_window.mainloop()

    except Exception as e:
        print(f"Error in admin_sign_in: {e}")

# Function to handle User Sign In
def user_sign_in():
    global current_window, current_user_id  # Declare the global variable
    try:
        sign_in_window.destroy()  # Close the previous window
        global user_sign_in_window
        user_sign_in_window = tk.Tk()
        user_sign_in_window.title("User Sign In")
        user_sign_in_window.configure(bg="#FAF9F6")

        tk.Label(user_sign_in_window, text="User Sign In", font=("Arial", 18, "bold"), bg="#FAF9F6").pack(pady=20)

        tk.Label(user_sign_in_window, text="Username", font=("Arial", 12), bg="#FAF9F6").pack(pady=5)
        user_username_entry = tk.Entry(user_sign_in_window, font=("Arial", 12), width=30)
        user_username_entry.pack(pady=5)

        tk.Label(user_sign_in_window, text="Password", font=("Arial", 12), bg="#FAF9F6").pack(pady=5)
        user_password_entry = tk.Entry(user_sign_in_window, font=("Arial", 12), width=30, show="*")
        user_password_entry.pack(pady=5)

        def handle_user_sign_in():
            global user, current_user_id
            username = user_username_entry.get()
            user = username
            password = user_password_entry.get()
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM Users WHERE Username = ? AND Password = ?', (username, password))
            result = cursor.fetchone()
            conn.close()

            # Check if a matching user exists
            if result:
                current_user_id = result[0]  # Store the user ID in the global variable
                print(f"User ID: {current_user_id}")
                print("User Sign In successful")
                open_main_app()  # Navigate to the main application
            else:
                messagebox.showerror("Error", "Invalid username or password. Try again.")
                print("Invalid credentials. Try again.")

        sign_in_btn = tk.Button(user_sign_in_window, text="Sign In", font=("Arial", 12), bg="#FF5722", fg="white", width=20, command=handle_user_sign_in)
        sign_in_btn.pack(pady=20)

        current_window = 'user_sign_in'

        # Center the window
        center_window(user_sign_in_window, 400, 400)

        user_sign_in_window.mainloop()

    except Exception as e:
        print(f"Error in user_sign_in: {e}")

# Function for Sign In page with Admin/User options
def open_sign_in():
    global current_window
    try:
        reg_window.destroy()  # Close the main registration window
        global sign_in_window
        sign_in_window = tk.Tk()
        sign_in_window.title("Sign In")
        sign_in_window.configure(bg="#FAF9F6")

        tk.Label(sign_in_window, text="Sign In", font=("Arial", 18, "bold"), bg="#FAF9F6").pack(pady=20)

        tk.Button(sign_in_window, text="Admin", font=("Arial", 12), bg="#FF5722", fg="white", width=20, command=admin_sign_in).pack(pady=20)
        tk.Button(sign_in_window, text="User", font=("Arial", 12), bg="#4CAF50", fg="white", width=20, command=user_sign_in).pack(pady=20)

        current_window = 'sign_in'

        # Center the window
        center_window(sign_in_window, 400, 300)

        sign_in_window.mainloop()

    except Exception as e:
        print(f"Error in open_sign_in: {e}")

# Function for Sign Up page
def open_sign_up():
    global current_window
    try:
        reg_window.destroy()  # Close the main registration window
        global sign_up_window
        sign_up_window = tk.Tk()
        sign_up_window.title("Sign Up")
        sign_up_window.configure(bg="#FAF9F6")

        tk.Label(sign_up_window, text="Sign Up", font=("Arial", 18, "bold"), bg="#FAF9F6").pack(pady=20)

        tk.Label(sign_up_window, text="New Username", font=("Arial", 12), bg="#FAF9F6").pack(pady=5)
        new_username_entry = tk.Entry(sign_up_window, font=("Arial", 12), width=30)
        new_username_entry.pack(pady=5)

        tk.Label(sign_up_window, text="New Password", font=("Arial", 12), bg="#FAF9F6").pack(pady=5)
        new_password_entry = tk.Entry(sign_up_window, font=("Arial", 12), width=30, show="*")
        new_password_entry.pack(pady=5)

        def handle_sign_up():
            global user, current_user_id
            new_username = new_username_entry.get()
            user = new_username
            new_password = new_password_entry.get()
            if(len(new_username)<6):
                if(new_username==""):
                    messagebox.showerror("error","username can't be empty")
                else:
                    messagebox.showerror("error","username can't be less than 6 characters")
            elif(len(new_password)<6):
                if(new_password==""):
                    messagebox.showerror("error","password can't be empty")
                else :
                    messagebox.showerror("error","password can't be less than 6 characters")
            else:
                if user_exists(new_username):
                    messagebox.showwarning("Sign up error","Username already exists. Please choose a different username.")
                    print("Username already exists. Please choose a different username.")
                else:
                # Insert the new user data into the database
                    insert_user(new_username, new_password)
                    conn = sqlite3.connect('user_data.db')
                    cursor = conn.cursor()
                    cursor.execute('SELECT id FROM Users WHERE Username = ? AND Password = ?', (new_username, new_password))
                    result = cursor.fetchone()
                    conn.close()
                    current_user_id = result[0]  # Store the user ID in the global variable
                    print(f"User ID: {current_user_id}")
                    open_main_app()
            # Check if the username already exists
        sign_up_btn = tk.Button(sign_up_window, text="Sign Up", font=("Arial", 12), bg="#2196F3", fg="white", width=20, command=handle_sign_up)
        sign_up_btn.pack(pady=20)

        current_window = 'sign_up'

        # Center the window
        center_window(sign_up_window, 400, 400)

        sign_up_window.mainloop()

    except Exception as e:
        print(f"Error in open_sign_up: {e}")

# Main registration screen with options
def create_registration_screen():
    global reg_window
    try:
        reg_window = tk.Tk()
        reg_window.title("Book Store - Registration")
        reg_window.configure(bg="#FAF9F6")
        icon = tk.PhotoImage(file = "books-piled-.png")
        reg_window.iconphoto(True,icon)

        tk.Label(reg_window, text="Welcome To Our Book Store", font=("Arial", 18, "bold"), bg="#FAF9F6").pack(pady=20)

        sign_in_btn = tk.Button(reg_window, text="Sign In", font=("Arial", 12), bg="#4CAF50", fg="white", width=20, command=open_sign_in)
        sign_in_btn.pack(pady=20)

        sign_up_btn = tk.Button(reg_window, text="Sign Up", font=("Arial", 12), bg="#2196F3", fg="white", width=20, command=open_sign_up)
        sign_up_btn.pack(pady=20)

        # Center the window
        center_window(reg_window, 400, 300)

        reg_window.mainloop()
    except Exception as e:
        print(f"Error in create_registration_screen: {e}")
        
#####################
def log_out():
    root.destroy()  # Close the main app window
    from registration import create_registration_screen
    create_registration_screen()  # Open the registration screen



def create_main_app():
    global root
    root = tk.Tk()
    root.title("Book Store App")
    root.geometry("1200x800")
    root.configure(bg="#FAF9F6")

    # Sidebar
    sidebar = tk.Frame(root, bg="#FCE6C9", width=250)
    sidebar.pack(side="left", fill="y")

    # Fetch user image path from the database
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT image_path FROM users WHERE username = ?", (user,))
    result = cursor.fetchone()
    image_path = result[0] if result else None

    # User Info
    if image_path and os.path.exists(image_path):
        user_img = Image.open(image_path).resize((50, 50))
        user_img_tk = ImageTk.PhotoImage(user_img)
    else:
        # Default image if the user has no profile picture
        user_img = Image.open("icons/user.png").resize((50, 50))  # Replace with your default image
        user_img_tk = ImageTk.PhotoImage(user_img)

    user_img_label = tk.Label(sidebar, image=user_img_tk, bg="#FCE6C9")
    user_img_label.image = user_img_tk  # Keep a reference to avoid garbage collection
    user_img_label.pack(pady=20)

    tk.Label(sidebar, text=user, font=("Arial", 14, "bold"), bg="#FCE6C9").pack()
    logout_btn = tk.Button(sidebar, text="LOG OUT", font=("Arial", 10), bg="black", fg="white", relief="flat", command=log_out)
    logout_btn.pack(pady=10)

    # Sidebar Menu
    menu_items = [
        {"name": "Home", "icon": "icons/home.png"},
        {"name": "Categories", "icon": "icons/options-lines.png"},
        {"name": "Saved", "icon": "icons/bookmark.png"},
        {"name": "Recommendations", "icon": "icons/advice.png"},
        {"name": "Reviews", "icon": "icons/positive-review.png"},
        {"name": "Settings", "icon": "icons/settings.png"},
        {"name": "Profile", "icon": "icons/user.png"},
        {"name": "Cart", "icon": "grocery-store.png"},
    ]
    main_frame = tk.Frame(root, bg="#FAF9F6")
    main_frame.pack(side="right", fill="both", expand=True)

    for item in menu_items:
        icon = Image.open(item["icon"]).resize((20, 20))
        icon_tk = ImageTk.PhotoImage(icon)

        btn = tk.Button(
            sidebar,
            text=item["name"],
            image=icon_tk,
            compound="left",
            font=("Arial", 12),
            bg="#FCE6C9",
            anchor="w",
            relief="flat",
            padx=20,
            activebackground='#FCE6C9',
            command=lambda name=item["name"]: show_profile_page(main_frame, user) if name == "Profile" else (
                show_home_page(main_frame) if name == "Home" else (
                    setting_page( main_frame,user) if name == "Settings" else (
                        show_cart_page(main_frame,current_user_id) if name == "Cart" else None
                    )
                )
            )
        )
        btn.image = icon_tk  # Keep a reference to prevent garbage collection
        btn.pack(fill="x", pady=5)

    # Main Content
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

    root.mainloop()
# Call this function to create the database at the beginning
create_database()
if __name__ == "__main__":
    # Start the registration screen
    create_registration_screen()