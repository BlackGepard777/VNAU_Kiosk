# update_admin_password.py
import database

# Змініть пароль для користувача 'admin'
admin_username = "admin"
new_admin_password = "dyfersjcr97531"

if database.update_user_password(admin_username, new_admin_password):
    print(f"Пароль для користувача '{admin_username}' успішно оновлено!")
else:
    print(f"Користувача '{admin_username}' не знайдено.")