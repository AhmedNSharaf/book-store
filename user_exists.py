import sqlite3


def user_exists(username):
    try:
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()

        # Query to check if the username already exists
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()  # Fetch the first result

        conn.close()

        if existing_user:
            return True  # User exists
        else:
            return False  # User does not exist
    except Exception as e:
        print(f"Error checking user existence: {e}")
        return False
