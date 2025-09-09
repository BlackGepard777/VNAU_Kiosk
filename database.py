import sqlite3
import bcrypt

DB_FOLDER = "./data/"

DB_NAME = "{}/videos.db".format(DB_FOLDER)
BG_name = "{}/background.db".format(DB_FOLDER)
USERS_DB = "{}/users.db".format(DB_FOLDER)

def get_user_connection():
    return sqlite3.connect(USERS_DB, check_same_thread=False)

def get_video_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

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

def init_videos_db():
    conn = get_video_connection()
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        yt_id TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        faculty TEXT NOT NULL
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS idle_videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        yt_id TEXT NOT NULL,
        title TEXT,
        is_active BOOLEAN NOT NULL CHECK (is_active IN (0, 1)) DEFAULT 0
    )
    ''')
    conn.commit()
    conn.close()

def video_exists(yt_id):
    """
    Перевіряє, чи існує відео з таким yt_id в базі даних.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM videos WHERE yt_id = ?", (yt_id,))
        exists = cursor.fetchone() is not None
        return exists
    except sqlite3.Error as e:
        print(f"Помилка бази даних: {e}")
        return False
    finally:
        if conn:
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


def add_video(yt_id, title, description, faculty):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO videos (yt_id, title, description, faculty) VALUES (?, ?, ?, ?)", 
              (yt_id, title, description, faculty))
    conn.commit()
    conn.close()

def get_videos(faculty=None, limit=5, offset=0):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if faculty:
        c.execute("SELECT id, yt_id, title, description, faculty FROM videos WHERE faculty=? LIMIT ? OFFSET ?", 
                  (faculty, limit, offset))
    else:
        c.execute("SELECT id, yt_id, title, description, faculty FROM videos LIMIT ? OFFSET ?", 
                  (limit, offset))
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "yt_id": r[1], "title": r[2], "description": r[3], "faculty": r[4]} for r in rows]

def count_videos(faculty=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if faculty:
        c.execute("SELECT COUNT(*) FROM videos WHERE faculty=?", (faculty,))
    else:
        c.execute("SELECT COUNT(*) FROM videos")
    count = c.fetchone()[0]
    conn.close()
    return count


def update_video(video_id, yt_id, title, description, faculty):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE videos SET yt_id=?, title=?, description=?, faculty=? WHERE id=?", 
              (yt_id, title, description, faculty, video_id))
    conn.commit()
    conn.close()

def delete_video(video_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM videos WHERE id=?", (video_id,))
    conn.commit()
    conn.close()

def add_idle_video(yt_id, title):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO idle_videos (yt_id, title) VALUES (?, ?)", (yt_id, title))
    conn.commit()
    conn.close()

def get_idle_videos():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM idle_videos ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "yt_id": r[1], "title": r[2], "is_active": r[3]} for r in rows]

def toggle_idle_video_status(video_id, status):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE idle_videos SET is_active = ? WHERE id = ?", (status, video_id))
    conn.commit()
    conn.close()

def delete_idle_video(video_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM idle_videos WHERE id = ?", (video_id,))
    conn.commit()
    conn.close()

def get_active_idle_video():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT yt_id FROM idle_videos WHERE is_active = 1 LIMIT 1")
    row = c.fetchone()
    conn.close()
    return row[0] if row else None