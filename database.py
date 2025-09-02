import sqlite3

DB_NAME = "videos.db"
BG_name = "background.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
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