import sqlite3

DATABASE_NAME = "kiosk.db"

def get_db_connection():
    """Створює з'єднання з базою даних."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Це дозволяє отримувати дані як словник
    return conn

def init_db():
    """Створює базу даних та таблицю `videos`, якщо вони не існують."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY,
            youtube_id TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT
        );
    ''')
    conn.commit()
    conn.close()

def seed_db():
    """Видаляє старі дані та вставляє нові відео."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM videos;")
    
    videos_data = [
        ('oAj63ct7IVM', 'куплінов', 'Вступний курс з основ програмування.'),
        ('zLpMh07eC88', 'топ', 'Відмінна пісня для відпочинку.'),
        ('iik25wqIufo', 'Ще одне відео', 'Це просто ще один приклад для демонстрації.')
    ]
    
    c.executemany("INSERT INTO videos (youtube_id, title, description) VALUES (?, ?, ?)", videos_data)
    conn.commit()
    print("База даних оновлена згідно з кодом.")
    conn.close()

def get_all_videos():
    """Повертає всі відео з бази даних."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT youtube_id, title, description FROM videos")
    videos = c.fetchall()
    conn.close()
    return [dict(row) for row in videos]