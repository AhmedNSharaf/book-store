import sqlite3


def get_balance(username):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT balance FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        if result:
            return result[0]  # Return the balance
        else:
            return 0.0  # Default balance if user not found
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return 0.0
    finally:
        conn.close()