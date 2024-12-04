import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3

# Database setup
def create_order_summary_window():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()

    def display_data():
        # Clear existing rows in the Treeview
        for row in tree.get_children():
            tree.delete(row)

        # Fetch data from the database
        cursor.execute("SELECT id, first_name, last_name, email, total FROM checkout")
        rows = cursor.fetchall()

        # Insert data into the Treeview
        for row in rows:
            tree.insert("", "end", values=row)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS checkout (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        address TEXT,
        governorate TEXT,
        country TEXT,
        phone_code TEXT,
        phone_number TEXT,
        payment_method TEXT,
        discount_code TEXT,
        total REAL
    )
    """)
    conn.commit()

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

    cart = []

    def update_governorate_options(combo_country, combo_governorate):
        selected_country = combo_country.get()
        if selected_country in countries_and_governorates:
            combo_governorate["values"] = countries_and_governorates[selected_country]
            combo_governorate.config(state="readonly")
        else:
            combo_governorate["values"] = []
            combo_governorate.config(state="disabled")

    def confirm_order():
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

        if not all([first_name, last_name, email, address, governorate, country, phone_code, phone_number, payment_method]):
            show_custom_message("Error", "Please fill in all required fields.")
            return

        cursor.execute("""
        INSERT INTO checkout (first_name, last_name, email, address, governorate, country, phone_code, phone_number, payment_method, discount_code)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (first_name, last_name, email, address, governorate, country, phone_code, phone_number, payment_method, discount_code))
        conn.commit()

        root.quit()

    def show_custom_message(title, message):
        custom_dialog = tk.Toplevel(root)
        custom_dialog.title(title)
        custom_dialog.geometry("300x150")
        custom_dialog.configure(bg="#ffffff")
        custom_dialog.overrideredirect(True)
        window_width = 300
        window_height = 150
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        custom_dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
        label_title = tk.Label(custom_dialog, text=title, font=("Arial", 16, "bold"), bg="#ffffff")
        label_title.pack(pady=10)
        label_message = tk.Label(custom_dialog, text=message, font=("Arial", 12), bg="#ffffff", wraplength=280)
        label_message.pack(pady=10)
        button_ok = tk.Button(custom_dialog, text="OK", command=custom_dialog.destroy, bg="green", fg="white", font=("Arial", 12))
        button_ok.pack(pady=10)
        

    root = tk.Tk()
    root.title("Order Summary")
    root.geometry("800x600")
    root.eval('tk::PlaceWindow . center')

    # Create a canvas and scrollbar for scrollable content
    canvas = tk.Canvas(root)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    scrollable_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Title Label
    label_title = tk.Label(scrollable_frame, text="Order Summary", font=("Arial", 20, "bold"))
    label_title.pack(pady=10)


    # Create frame for Treeview
    frame_orders = tk.Frame(scrollable_frame, padx=20, pady=10)
    frame_orders.pack(fill=tk.BOTH, expand=True)

    # Treeview setup for orders
    columns = ("ID", "First Name", "Last Name", "Email", "Total")
    tree = ttk.Treeview(frame_orders, columns=columns, show="headings")
    tree.heading("ID", text="Order ID")
    tree.heading("First Name", text="First Name")
    tree.heading("Last Name", text="Last Name")
    tree.heading("Email", text="Email")
    tree.heading("Total", text="Total ($)")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Display the data in the Treeview
    display_data()

    # Frame for Entry Widgets (Order Form)
    frame_order_form = tk.Frame(scrollable_frame)
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


    frame_buttons = tk.Frame(scrollable_frame, pady=20)
    frame_buttons.pack()

    tk.Button(frame_buttons, text="Confirm Order", command=confirm_order, bg="green", fg="white", font=("Arial", 14)).grid(row=0, column=0, padx=10)
    tk.Button(frame_buttons, text="Cancel", command=root.quit, bg="red", fg="white", font=("Arial", 14)).grid(row=0, column=1, padx=10)

    window_width = 800
    window_height = 600

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the x and y coordinates to position the window in the center
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the window geometry
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    root.mainloop()
create_order_summary_window()