from flask import Flask, render_template, jsonify, request, redirect, url_for
import database
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, unquote

app = Flask(__name__)

# ----------------- Публічні сторінки -----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/en")
def english():
    return render_template("usa.html")

@app.route("/faculties")
def faculties_page():
    return render_template("faculties.html")

@app.route("/video")
def video_page():
    faculty = request.args.get("faculty")
    return render_template("video.html", faculty=faculty)

@app.route("/api/videos")
def api_videos():
    page = int(request.args.get("page", 1))
    faculty = request.args.get("faculty")
    per_page = 5
    offset = (page - 1) * per_page

    videos = database.get_videos(faculty=faculty, limit=per_page, offset=offset)
    total = database.count_videos(faculty=faculty)

    return jsonify({
        "videos": videos,
        "page": page,
        "pages": (total + per_page - 1) // per_page
    })

# ----------------- Новини -----------------
@app.route('/news')
def news_page():
    return render_template('news.html')

@app.route('/api/news')
def get_news():
    url = "https://vsau.org/novini"
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        news_containers = soup.find_all("div", class_="node clearfix")
        news_articles = []
        for container in news_containers:
            title_link_element = container.find("a", href=True)
            content_element = container.find("p", class_="my-2")
            image_element = container.find("img")
            if title_link_element and content_element:
                news_articles.append({
                    "title": title_link_element.get_text(strip=True),
                    "link": urljoin(url, title_link_element["href"]),
                    "content": content_element.get_text(strip=True),
                    "image": urljoin(url, image_element["src"]) if image_element else None
                })
        return jsonify(news_articles)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/news/detail')
def get_news_detail():
    news_url = request.args.get("url")
    if not news_url:
        return jsonify({"error": "Не передано параметр url"}), 400
    news_url = unquote(news_url)
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(news_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        title_element = soup.find("h1", class_="title")
        title = title_element.get_text(strip=True) if title_element else "Без заголовку"
        content_element = soup.find("div", class_="content")
        paragraphs = content_element.find_all("p") if content_element else []
        content = "\n\n".join(p.get_text(strip=True) for p in paragraphs)
        image_element = content_element.find("img") if content_element else None
        image = urljoin(news_url, image_element["src"]) if image_element else None
        return jsonify({"title": title, "content": content, "image": image, "url": news_url})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# ----------------- Оголошення -----------------
# ----------------- Оголошення -----------------
@app.route('/api/announcements')
def get_announcements():
    """Отримує оголошення зі сторінки https://vsau.org/novini/ogoloshennya."""
    base_url = "https://vsau.org"
    url = f"{base_url}/novini/ogoloshennya"
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        announcement_containers = soup.find_all("div", class_="node clearfix")
        
        announcements = []
        for container in announcement_containers:
            title_link_element = container.find("a", href=True)
            if title_link_element:
                full_link = urljoin(base_url, title_link_element["href"])
                announcements.append({
                    "title": title_link_element.get_text(strip=True),
                    "link": full_link,  # передаємо повний URL
                    "content": "Для перегляду повного тексту, перейдіть за посиланням.",
                    "image": None
                })
        
        return jsonify(announcements)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500



@app.route('/api/announcements/detail')
def get_announcement_detail():
    announcement_url = request.args.get("url")
    if not announcement_url:
        return jsonify({"error": "Не передано параметр url"}), 400

    announcement_url = unquote(announcement_url)

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(announcement_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Заголовок
        title_element = soup.find("h1", class_="content-page-title") or soup.find("title")
        title = title_element.get_text(strip=True) if title_element else "Без заголовку"

        # Контент — шукаємо кілька можливих контейнерів
        content_element = (
            soup.find("div", class_="content-node-body") or
            soup.find("div", class_="field-items") or
            soup.find("article") or
            soup.find("div", class_="content")
        )

        content = "Контент не знайдено."
        if content_element:
            paragraphs = content_element.find_all(["p", "div", "li"])
            if paragraphs:
                content = "\n\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
            else:
                content = content_element.get_text(separator='\n\n', strip=True)

        return jsonify({"title": title, "content": content, "image": None, "url": announcement_url})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Помилка при завантаженні сторінки: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Помилка парсингу вмісту: {e}"}), 500



# ----------------- Розклад -----------------
@app.route("/schedule")
def schedule_page():
    return render_template("schedule.html")


#------------------Абітурієнтам---------------
@app.route("/abiturient")
def abiturient_page():
    return render_template("abiturient.html")

@app.route("/rules")
def rules_page():
    return render_template("abiturient_page_list/rules.html")

@app.route("/specialties")
def specialties_page():
    return render_template("abiturient_page_list/specialties.html")

@app.route("/admission")
def admission_page():
    return render_template("abiturient_page_list/admission.html")

@app.route("/documents")
def documents_page():
    return render_template("abiturient_page_list/documents.html")

@app.route("/contacts")
def contacts_page():
    return render_template("abiturient_page_list/contacts.html")

@app.route("/tuition")
def tuition_page():
    return render_template("abiturient_page_list/tuition.html")

@app.route("/studentlife")
def studentlife_page():
    return render_template("abiturient_page_list/studentlife.html")

@app.route("/about")
def about_page():
    return render_template("abiturient_page_list/about.html")

# ----------------- Адмінка -----------------
@app.route("/admin")
def admin_page():
    videos = database.get_videos(limit=1000, offset=0)
    faculties = [
        "Агрономія", "Екологія", "Інженерія", "Економіка",
        "Облік і фінанси", "Менеджмент", "Технології виробництва", "Ветеринарна медицина"
    ]
    return render_template("admin.html", videos=videos, faculties=faculties)

@app.route("/admin/add", methods=["POST"])
def admin_add():
    yt_id = request.form["yt_id"]
    title = request.form["title"]
    description = request.form["description"]
    faculty = request.form["faculty"]
    database.add_video(yt_id, title, description, faculty)
    return redirect(url_for("admin_page"))

@app.route("/admin/update/<int:video_id>", methods=["POST"])
def admin_update(video_id):
    yt_id = request.form["yt_id"]
    title = request.form["title"]
    description = request.form["description"]
    faculty = request.form["faculty"]
    database.update_video(video_id, yt_id, title, description, faculty)
    return redirect(url_for("admin_page"))

@app.route("/admin/delete/<int:video_id>", methods=["POST"])
def admin_delete(video_id):
    database.delete_video(video_id)
    return redirect(url_for("admin_page"))

# ----------------- YouTube API -----------------
@app.route('/api/get_video_info')
def get_video_info():
    yt_id = request.args.get("yt_id")
    if not yt_id:
        return jsonify({"error": "Не вказано YouTube ID."}), 400
    url = f"https://www.youtube.com/watch?v={yt_id}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.find("meta", property="og:title")
        description_tag = soup.find("meta", property="og:description")
        return jsonify({
            "title": title_tag["content"] if title_tag else "Без назви",
            "description": description_tag["content"] if description_tag else "Без опису"
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# ----------------- Запуск -----------------
if __name__ == "__main__":
    database.init_db()
    app.run(debug=True)