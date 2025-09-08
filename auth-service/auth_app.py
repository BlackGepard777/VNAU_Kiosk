from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from dotenv import load_dotenv
import requests
import auth_database
import os
import re

app = Flask(__name__)
load_dotenv() 
app.secret_key = os.getenv("SECRET_KEY")
print(f"Loaded SECRET_KEY: {'[value hidden]' if app.secret_key else None}")
USERS_DB = "users.db"

MAIN_SERVICE_URL = "http://127.0.0.1:5000"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = auth_database.get_user_by_credentials(username, password)
        
        if user:
            session['user'] = user
            return redirect(f"{MAIN_SERVICE_URL}/admin")
        else:
            return render_template("login.html", error="Невірний логін або пароль")
    
    if 'user' in session:
        return redirect(f"{MAIN_SERVICE_URL}/admin")
    
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(f"{MAIN_SERVICE_URL}/login")


@app.route("/api/check_session")
def check_session():
    if 'user' in session:
        return jsonify({
            'valid': True,
            'user': {
                'username': session['user']['username'],
                'role': session['user']['role']
            }
        })
    return jsonify({'valid': False})

if __name__ == "__main__":
    auth_database.init_users_db()
    app.run(debug=True, port=5001)