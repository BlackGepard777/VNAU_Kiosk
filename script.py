import database

if __name__ == "__main__":
    # створюємо всі таблиці, якщо їх ще немає

    username = "admin"
    password = "admin123"  # заміни на свій
    role = "admin"

    if database.create_user(username, password, role):
        print(f"✅ Адміна '{username}' створено з паролем '{password}'")
    else:
        print(f"⚠️ Користувач '{username}' уже існує у базі.")
