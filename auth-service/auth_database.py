import sqlite3
import bcrypt

USERS_DB = "users.db"

def get_user_connection():
    return sqlite3.connect(USERS_DB, check_same_thread=False)

def init_users_db():
    conn = get_user_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, stored_hash):
    try:
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
    except ValueError:
        return False

def create_user(username, password, role='user'):
    conn = get_user_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM users WHERE username=?", (username,))
    if cursor.fetchone():
        print(f"Користувач '{username}' уже існує. Створення скасовано.")
        conn.close()
        return False

    password_hash = hash_password(password)
    cursor.execute(
        'INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
        (username, password_hash, role)
    )
    conn.commit()
    conn.close()
    return True

def get_user_by_credentials(username, password):
    conn = get_user_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, password_hash, role FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user and verify_password(password, user[2]):
        return {
            'id': user[0],
            'username': user[1],
            'role': user[3]
        }
    return None

def update_user_password(username, new_password):
    conn = get_user_connection()
    cursor = conn.cursor()

    new_password_hash = hash_password(new_password)

    cursor.execute(
        'UPDATE users SET password_hash = ? WHERE username = ?',
        (new_password_hash, username)
    )
    conn.commit()
    conn.close()

    if cursor.rowcount > 0:
        return True
    return False