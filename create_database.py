import sqlite3


def create_database():
    conn = sqlite3.connect('user_data.db')  # Connect to SQLite database (or create it)
    cursor = conn.cursor()

    # Create a table to store user data if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL,
                        email TEXT,
                        balance REAL,
                        Purchase_Hist TEXT,
                        Shipping_Addr TEXT,
                        image_path TEXT
                        )''')
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS admins(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL,
                        email TEXT,
                        admin_key TEXT NOT NULL
                    )
                    ''')
    # Books Table
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Books (
                        ISBN TEXT PRIMARY KEY,
                        Title TEXT NOT NULL,
                        Category TEXT,
                        Author TEXT NOT NULL,
                        Genre TEXT,
                        Publication TEXT,
                        Price REAL,
                        Date_Last_Purchased TEXT
                    )
                ''')
    # Orders Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            Order_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Order_Date TEXT NOT NULL,
            Delivery_Date TEXT,
            Total_Cost REAL NOT NULL,
            Done BOOLEAN DEFAULT 0,
            Quantity INTEGER ,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            address TEXT,
            governorate TEXT,
            country TEXT,
            phone_code TEXT,
            phone_number TEXT,
            payment_method TEXT,
            discount_code TEXT
        )
    ''')
    
        # Shipping & Delivery Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Shipping_Delivery (
            Order_ID INTEGER,
            Shipping_Status TEXT,
            Delivery_Date TEXT,
            FOREIGN KEY (Order_ID) REFERENCES Orders (Order_ID)
        )
    ''')
    # Reviews & Ratings Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reviews_Ratings (
            ISBN TEXT,
            Customer_ID INTEGER,
            Rating INTEGER,
            Review TEXT,
            FOREIGN KEY (ISBN) REFERENCES Books (ISBN),
            FOREIGN KEY (Customer_ID) REFERENCES Customers (Customer_ID)
        )
    ''')
    conn.commit()
    conn.close()
    
    