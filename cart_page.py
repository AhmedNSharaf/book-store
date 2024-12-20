import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk




def create_cart_table():
    # Create a temporary table for the cart
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cart (
            Cart_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ISBN TEXT NOT NULL,
            Title TEXT,
            Quantity INTEGER,
            Price REAL,
            FOREIGN KEY (ISBN) REFERENCES Books (ISBN)
        )
    ''')
    conn.commit()
    conn.close()


def show_cart_page(main_frame,current_user_id):
    # Clear the main frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Cart Page Content
    cart_frame = tk.Frame(main_frame, bg="#FAF9F6")
    cart_frame.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(cart_frame, text="Your Cart", font=("Arial", 18, "bold"), bg="#FAF9F6").pack(pady=10)

    # Cart Table
    columns = ("ISBN", "Title", "Quantity", "Price", "Total")
    cart_table = ttk.Treeview(cart_frame, columns=columns, show="headings", height=10)
    for col in columns:
        cart_table.heading(col, text=col)
    cart_table.pack(pady=10, fill="x")

    # Function to fetch and display cart contents
    def load_cart():
        cart_table.delete(*cart_table.get_children())
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT ISBN, Title, Quantity, Price, Quantity * Price AS Total FROM Cart')
        for row in cursor.fetchall():
            cart_table.insert("", "end", values=row)
        conn.close()

    load_cart()

    # Function to add books to the cart
    def add_to_cart():
        # Create a popup window for selecting a book
        cart_window = tk.Toplevel()
        cart_window.title("Add to Cart")
        cart_window.geometry("400x250")
        cart_window.configure(bg="#FAF9F6")

        tk.Label(cart_window, text="Select a book to add to the cart:", font=("Arial", 12), bg="#FAF9F6").pack(pady=10)

        # Connect to the database to fetch books
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT ISBN, Title, Price FROM Books')
        books = cursor.fetchall()
        conn.close()

        # Create a dictionary to map book titles to their ISBN and price
        book_dict = {book[1]: (book[0], book[2]) for book in books}

        # Create a dropdown list with book titles
        book_dropdown = ttk.Combobox(cart_window, state="readonly", font=("Arial", 12), width=30)
        book_dropdown['values'] = list(book_dict.keys())
        book_dropdown.pack(pady=10)

        # Input field for quantity
        tk.Label(cart_window, text="Enter Quantity:", font=("Arial", 12), bg="#FAF9F6").pack(pady=5)
        quantity_entry = tk.Entry(cart_window, font=("Arial", 12), width=10, justify="center")
        quantity_entry.pack(pady=5)

        def handle_add_to_cart():
            selected_title = book_dropdown.get()
            quantity = quantity_entry.get()

            if not selected_title:
                messagebox.showerror("Error", "Please select a book.")
                return

            if not quantity.isdigit() or int(quantity) <= 0:
                messagebox.showerror("Error", "Please enter a valid quantity (greater than 0).")
                return

            quantity = int(quantity)
            isbn, price = book_dict[selected_title]

            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()

            # Check if the book is already in the cart
            cursor.execute('SELECT Quantity FROM Cart WHERE ISBN = ?', (isbn,))
            existing = cursor.fetchone()
            if existing:
                # Update quantity if the book is already in the cart
                cursor.execute('UPDATE Cart SET Quantity = Quantity + ? WHERE ISBN = ?', (quantity, isbn))
            else:
                # Add the book to the cart with the specified quantity
                cursor.execute('INSERT INTO Cart (ISBN, Title, Quantity, Price) VALUES (?, ?, ?, ?)',
                               (isbn, selected_title, quantity, price))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"'{selected_title}' has been added to your cart (Quantity: {quantity}).")
            cart_window.destroy()  # Close the pop-up window
            load_cart()  # Refresh the cart display

        # Add button to confirm selection
        tk.Button(cart_window, text="Add to Cart", font=("Arial", 12), bg="#4CAF50", fg="white", command=handle_add_to_cart).pack(pady=20)

    # Function to remove books from the cart
    def remove_from_cart():
        selected_item = cart_table.selection()
        if selected_item:
            isbn = cart_table.item(selected_item, "values")[0]
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Cart WHERE ISBN = ?', (isbn,))
            conn.commit()
            conn.close()
            load_cart()
            messagebox.showinfo("Removed", "Item removed from cart.")
        else:
            messagebox.showwarning("No Selection", "Please select an item to remove.")

    # Function to proceed to checkout
    def checkout():
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()

        # Calculate total cost and total quantity
        cursor.execute('SELECT SUM(Quantity * Price), SUM(Quantity) FROM Cart')
        result = cursor.fetchone()
        total_cost = result[0]
        total_quantity = result[1]
        
        # Get the current user's balance
        cursor.execute('SELECT balance FROM users WHERE id = ?', (current_user_id,))
        user_balance = cursor.fetchone()[0]

        # Check if the user has sufficient balance
        if user_balance < total_cost:
            messagebox.showerror("Insufficient Balance", "You do not have enough balance to complete this purchase.")
            conn.close()
            return  # Exit the function if balance is insufficient

        # Deduct total cost from user's balance
        cursor.execute('UPDATE users SET balance = balance - ? WHERE id = ?', (total_cost, current_user_id))

        # Get shipping and payment details
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        email = entry_email.get()
        address = entry_address.get()
        governorate = combo_governorate.get()
        country = combo_country.get()
        phone_code = phone_code_combo.get()
        phone_number = entry_phone_number.get()
        payment_method = combo_payment.get()
        discount_code = entry_discount.get()

        # Check if all required fields are filled
        if total_cost:
            if not all([first_name, last_name, email, address, governorate, country, phone_code, phone_number, payment_method]):
                messagebox.showerror("Error", "Please fill in all required fields.")
                return
            else:
                # Insert a new order into the Orders table
                cursor.execute(
                    'INSERT INTO Orders (Order_Date, Total_Cost, Quantity, first_name, last_name, email, address, governorate, country, phone_code, phone_number, payment_method, discount_code, user_id) VALUES (DATE("now"), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (total_cost, total_quantity, first_name, last_name, email, address, governorate, country, phone_code, phone_number, payment_method, discount_code, current_user_id)
                )
                order_id = cursor.lastrowid
                conn.commit()

                messagebox.showinfo(
                    "Checkout Successful", f"Order #{order_id} placed. Total cost: ${total_cost:.2f}, Total quantity: {total_quantity}."
                )

                # Clear the cart and reload the cart view
                clear_cart()
                load_cart()

        else:
            messagebox.showwarning("Empty Cart", "Your cart is empty.")

        conn.close()



    # Function to clear the cart
    def clear_cart():
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Cart')
        conn.commit()
        conn.close()

    ################
    countries_and_governorates = {
        "USA": ["California", "Texas", "Florida", "New York", "Illinois", "Pennsylvania", "Ohio", "Georgia", "North Carolina", "Michigan"],
        "Canada": ["Ontario", "Quebec", "British Columbia", "Alberta", "Manitoba", "Saskatchewan", "Nova Scotia", "New Brunswick", "Prince Edward Island", "Newfoundland and Labrador"],
        "Egypt": ["Cairo", "Alexandria","Ismailia", "Giza", "Qalyubia", "Dakahlia", "Sharqia", "Gharbia", "Beheira", "Fayoum", "Aswan"],
        "UK": ["England", "Scotland", "Wales", "Northern Ireland"],
        "India": ["Andhra Pradesh", "Bihar", "Gujarat", "Karnataka", "Madhya Pradesh", "Maharashtra", "Rajasthan", "Tamil Nadu", "Uttar Pradesh", "West Bengal"],
        "Australia": ["New South Wales", "Victoria", "Queensland", "South Australia", "Western Australia", "Tasmania", "Australian Capital Territory", "Northern Territory"],
        "Germany": ["Bavaria", "Berlin", "Brandenburg", "Hesse", "North Rhine-Westphalia", "Saxony", "Baden-Württemberg", "Lower Saxony", "Rhineland-Palatinate", "Thuringia"],
        "France": ["Île-de-France", "Provence-Alpes-Côte d'Azur", "Auvergne-Rhône-Alpes", "Nouvelle-Aquitaine", "Occitanie", "Hauts-de-France", "Grand Est", "Normandy", "Brittany", "Pays de la Loire"],
        "Italy": ["Lazio", "Lombardy", "Veneto", "Campania", "Sicily", "Piedmont", "Emilia-Romagna", "Tuscany", "Apulia", "Calabria"],
        "Japan": ["Tokyo", "Osaka", "Hokkaido", "Aichi", "Kanagawa", "Saitama", "Chiba", "Hyogo", "Fukuoka", "Okinawa"],
        "Mexico": ["CDMX (Mexico City)", "Jalisco", "Nuevo León", "Puebla", "Chihuahua", "Guerrero", "Sonora", "Baja California", "Yucatan", "Veracruz"],
        "Brazil": ["São Paulo", "Rio de Janeiro", "Minas Gerais", "Bahia", "Paraná", "Santa Catarina", "Ceará", "Pernambuco", "Goías", "Espírito Santo"],
        "Russia": ["Moscow", "Saint Petersburg", "Tatarstan", "Sverdlovsk", "Krasnoyarsk", "Primorsky Krai", "Chelyabinsk", "Novosibirsk", "Krasnodar", "Omsk"],
        "China": ["Beijing", "Shanghai", "Guangdong", "Zhejiang", "Jiangsu", "Shandong", "Hebei", "Henan", "Sichuan", "Hunan"],
        "South Africa": ["Western Cape", "Eastern Cape", "Gauteng", "KwaZulu-Natal", "Free State", "Limpopo", "Mpumalanga", "North West", "Northern Cape"],
        "Spain": ["Madrid", "Catalonia", "Andalusia", "Valencia", "Galicia", "Basque Country", "Castile and León", "Castilla-La Mancha", "Murcia", "Aragon"],
        "Argentina": ["Buenos Aires", "CABA (Buenos Aires City)", "Santa Fe", "Mendoza", "Córdoba", "Tucumán", "Salta", "Entre Ríos", "Chaco", "Misiones"],
        "South Korea": ["Seoul", "Busan", "Incheon", "Daegu", "Gwangju", "Daejeon", "Ulsan", "Gyeonggi", "Gangwon", "Jeolla"],
        "Turkey": ["Istanbul", "Ankara", "Izmir", "Antalya", "Bursa", "Adana", "Gaziantep", "Konya", "Mersin", "Şanlıurfa"],
        "Saudi Arabia": ["Riyadh", "Mecca", "Medina", "Eastern Province", "Jeddah", "Asir", "Najran", "Qassim", "Al Baha", "Tabuk"]
    }

    country_codes = {
        "Egypt": "+20",
        "USA": "+1",
        "UK": "+44",
        "Canada": "+1",
        "India": "+91",
        "Australia": "+61",
        "Germany": "+49",
        "France": "+33",
        "Italy": "+39",
        "Japan": "+81",
        "Mexico": "+52",
        "Brazil": "+55",
        "Russia": "+7",
        "China": "+86",
        "South Africa": "+27",
        "Spain": "+34",
        "Argentina": "+54",
        "South Korea": "+82",
        "Turkey": "+90",
        "Saudi Arabia": "+966"
    }
    def update_governorate_options(combo_country, combo_governorate):
        selected_country = combo_country.get()
        if selected_country in countries_and_governorates:
            combo_governorate["values"] = countries_and_governorates[selected_country]
            combo_governorate.config(state="readonly")
        else:
            combo_governorate["values"] = []
            combo_governorate.config(state="disabled")

    frame_order_form = tk.Frame(cart_frame)
    frame_order_form.pack(pady=10)

    # First Name
    label_first_name = tk.Label(frame_order_form, text="First Name")
    label_first_name.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_first_name = tk.Entry(frame_order_form, width=30)
    entry_first_name.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # Last Name
    label_last_name = tk.Label(frame_order_form, text="Last Name")
    label_last_name.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_last_name = tk.Entry(frame_order_form, width=30)
    entry_last_name.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    # Email
    label_email = tk.Label(frame_order_form, text="Email")
    label_email.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_email = tk.Entry(frame_order_form, width=30)
    entry_email.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    # Address
    label_address = tk.Label(frame_order_form, text="Address")
    label_address.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entry_address = tk.Entry(frame_order_form, width=30)
    entry_address.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    # Country
    label_country = tk.Label(frame_order_form, text="Country")
    label_country.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    combo_country = ttk.Combobox(frame_order_form, values=list(countries_and_governorates.keys()), width=27)
    combo_country.grid(row=4, column=1, padx=10, pady=5, sticky="w")
    combo_country.bind("<<ComboboxSelected>>", lambda event: update_governorate_options(combo_country, combo_governorate))

    # Governorate
    label_governorate = tk.Label(frame_order_form, text="Governorate")
    label_governorate.grid(row=5, column=0, padx=10, pady=5, sticky="w")
    combo_governorate = ttk.Combobox(frame_order_form,width=27)
    combo_governorate.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    # Phone Number
    label_phone_number = tk.Label(frame_order_form, text="Phone Number")
    label_phone_number.grid(row=6, column=0, padx=10, pady=5, sticky="w")

    # Create a frame for phone code and number
    frame_phone_number = tk.Frame(frame_order_form)
    frame_phone_number.grid(row=6, column=1, padx=5, pady=5, sticky="w")  # Place this in column 1

    # Phone Code (smaller width)
    phone_code_combo = ttk.Combobox(frame_phone_number, values=list(country_codes.values()), width=5)
    phone_code_combo.pack(side="left", padx=5)

    # Phone Number Entry (larger width)
    entry_phone_number = tk.Entry(frame_phone_number, width=20)
    entry_phone_number.pack(side="left", padx=2)




    # Payment Method
    label_payment_method = tk.Label(frame_order_form, text="Payment Method")
    label_payment_method.grid(row=8, column=0, padx=10, pady=5, sticky="w")
    combo_payment = ttk.Combobox(frame_order_form, values=["Credit Card", "PayPal", "Bank Transfer", "Cash on Delivery"],width=27)
    combo_payment.grid(row=8, column=1, padx=10, pady=5, sticky="w")

    # Discount Code
    label_discount = tk.Label(frame_order_form, text="Discount Code (optional)")
    label_discount.grid(row=9, column=0, padx=10, pady=5, sticky="w")
    entry_discount = tk.Entry(frame_order_form,width=30)
    entry_discount.grid(row=9, column=1, padx=10, pady=5, sticky="w")

    def clear_input_fields():
        # Clear all text entries
        entry_first_name.delete(0, tk.END)
        entry_last_name.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_address.delete(0, tk.END)
        entry_phone_number.delete(0, tk.END)
        entry_discount.delete(0, tk.END)

        # Reset combobox selections
        combo_country.set("")
        combo_governorate.set("")
        phone_code_combo.set("")
        combo_payment.set("")

    ################



    # Buttons
    button_frame = tk.Frame(cart_frame, bg="#FAF9F6")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Add to Cart", bg="#4CAF50", fg="white", font=("Arial", 12), command=add_to_cart).pack(side="left", padx=5)
    tk.Button(button_frame, text="Remove Selected", bg="#FF5722", fg="white", font=("Arial", 12), command=remove_from_cart).pack(side="left", padx=5)
    tk.Button(button_frame, text="Checkout", bg="#007BFF", fg="white", font=("Arial", 12), command=checkout).pack(side="left", padx=5)


# Create the database and cart table
create_cart_table()
