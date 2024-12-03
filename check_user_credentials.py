import sqlite3


def check_user_credentials(username, password):
    try:
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()

        # Query to find user by username and password
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()  # Fetch the first result

        conn.close()

        if user:
            return True  # User found and credentials are correct
        else:
            return False  # Invalid credentials
    except Exception as e:
        print(f"Error checking user credentials: {e}")
        return False



def check_admin_credentials(username,password,admin_key):
    try:
        conn = sqlite3.connect('user_data.db')
        cursor= conn.cursor()
        cursor.execute('SELECT * FROM admins WHERE username = ? AND password = ? AND admin_key = ?', (username, password,admin_key))
        admin = cursor.fetchone()
        conn.close()
        
        if admin:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking admin credentials: {e}")
        return False
