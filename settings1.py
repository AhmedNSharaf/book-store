import tkinter as tk
from tkinter import messagebox
# Function to clear the current frame and show a new one                   
def show_page(page_function, main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()  # Remove existing widgets
    page_function(main_frame)

# Settings Page Function
def show_settings_page(main_frame):
    # Clear the main frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Settings Page Frame
    settings_frame = tk.Frame(main_frame, bg="#FAF9F6")
    settings_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Title for the settings page
    tk.Label(settings_frame, text="Settings", font=("Arial", 24, "bold"), bg="#FAF9F6", fg="#333").pack(pady=(10, 20))

    # Account Section
    tk.Label(settings_frame, text="Account Settings", font=("Arial", 18, "bold"), bg="#FAF9F6", fg="#4CAF50").pack(anchor="w", pady=(10, 5))
    tk.Button(settings_frame, text="Update Username/Password", font=("Arial", 14), bg="#4CAF50", fg="white", 
              command=lambda: messagebox.showinfo("Account", "Update Username/Password")).pack(fill="x", padx=10, pady=5)
    tk.Button(settings_frame, text="Manage Payment Methods", font=("Arial", 14), bg="#4CAF50", fg="white", 
              command=lambda: messagebox.showinfo("Payments", "Manage Payment Methods")).pack(fill="x", padx=10, pady=5)

    # Preferences Section
    tk.Label(settings_frame, text="Preferences", font=("Arial", 18, "bold"), bg="#FAF9F6", fg="#4CAF50").pack(anchor="w", pady=(20, 5))
    
    genres = ["Fiction", "Non-Fiction", "Mystery", "Science Fiction", "Fantasy"]
    selected_genre = tk.StringVar(value="Fiction")

    tk.Label(settings_frame, text="Preferred Genre:", font=("Arial", 14), bg="#FAF9F6", fg="#333").pack(anchor="w", pady=(5, 5))
    genre_menu = tk.OptionMenu(settings_frame, selected_genre, *genres)
    genre_menu.config(font=("Arial", 12), bg="#FAF9F6", fg="#333")
    genre_menu.pack(anchor="w", padx=10, pady=(0, 10))

    tk.Label(settings_frame, text="Preferred Currency:", font=("Arial", 14), bg="#FAF9F6", fg="#333").pack(anchor="w", pady=(5, 5))
    currency_var = tk.StringVar(value="USD")
    tk.Entry(settings_frame, textvariable=currency_var, font=("Arial", 12), bg="#FFFFFF").pack(anchor="w", padx=10, pady=(0, 10))

    # Notifications Toggle
    notifications_var = tk.BooleanVar(value=True)
    tk.Checkbutton(settings_frame, text="Enable Email Notifications", variable=notifications_var, font=("Arial", 14), bg="#FAF9F6", fg="#333").pack(anchor="w", pady=10)

    # Display Options
    tk.Label(settings_frame, text="Display Options", font=("Arial", 18, "bold"), bg="#FAF9F6", fg="#4CAF50").pack(anchor="w", pady=(20, 5))
    font_size_var = tk.IntVar(value=12)
    tk.Label(settings_frame, text="Font Size:", font=("Arial", 14), bg="#FAF9F6", fg="#333").pack(anchor="w", pady=(5, 5))
    tk.Scale(settings_frame, from_=8, to=24, orient="horizontal", variable=font_size_var, bg="#FAF9F6").pack(anchor="w", pady=(0, 10))

    # Save Settings Button
    def save_settings():
        preferences = {
            "genre": selected_genre.get(),
            "currency": currency_var.get(),
            "notifications": notifications_var.get(),
            "font_size": font_size_var.get(),
        }
        # Save preferences logic (e.g., update database or write to a file)
        messagebox.showinfo("Settings Saved", f"Your preferences have been updated:\n{preferences}")

    tk.Button(settings_frame, text="Save Settings", font=("Arial", 14), bg="#4CAF50", fg="white", command=save_settings).pack(pady=(20, 10), fill="x", padx=10)

    # Button to go back to previous settings (optional)
    tk.Button(settings_frame, text="Back to Previous Page", font=("Arial", 14), bg="#FF5722", fg="white", 
                command=lambda: show_page(show_settings_page, main_frame)).pack(pady=4, fill="x", padx=10)

# Main function to start the application
def main():
    show_page(show_settings_page, root)  # Initially show the settings page

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Book Store Application")
    root.geometry("800x600")
    main()
    root.mainloop()