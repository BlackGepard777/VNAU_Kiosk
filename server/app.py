from flask import Flask, jsonify, request, send_from_directory
import os
import database

# Визначаємо абсолютний шлях до кореневої папки проєкту.
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Створюємо Flask-додаток, вказуючи, що статичні файли знаходяться у підпапці 'assets'
# URL-адреси до цих файлів будуть починатися з /assets
app = Flask(__name__, 
            static_folder=os.path.join(root_dir, 'assets'),
            static_url_path='/assets')

# Маршрут для головної сторінки (index.html), яка знаходиться в корені
@app.route('/')
def serve_index():
    return send_from_directory(root_dir, 'index.html')

# Маршрут для обслуговування файлів з папки 'pages'
@app.route('/pages/<path:filename>')
def serve_pages(filename):
    return send_from_directory(os.path.join(root_dir, 'pages'), filename)

# API-маршрут для отримання даних про відео
@app.route('/api/videos')
def get_videos():
    videos = database.get_all_videos()
    return jsonify(videos)

# API-маршрут для видалення відео
@app.route('/api/videos/<int:video_id>', methods=['DELETE'])
def delete_video(video_id):
    conn = database.get_db_connection()
    conn.execute('DELETE FROM videos WHERE id = ?', (video_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Відео успішно видалено'}), 200

if __name__ == '__main__':
    database.init_db()
    database.seed_db()
    app.run(debug=True, port=5000)