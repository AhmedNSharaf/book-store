import sqlite3


def insert_user(username, password):
    try:
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()

        # Insert user into the table
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))

        conn.commit()
        conn.close()

        print("User registered successfully")
    except Exception as e:
        print(f"Error inserting user: {e}")
