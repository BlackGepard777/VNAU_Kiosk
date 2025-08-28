import sqlite3

DB_NAME = "videos.db"

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
