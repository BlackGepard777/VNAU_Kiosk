from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask import Blueprint
import database
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, unquote
from dotenv import load_dotenv
import os
import re



kiosk_bp = Blueprint('kiosk_bp', __name__)

@kiosk_bp.route("/")
def home():
    return render_template("index.html")


@kiosk_bp.route("/idle")
def idle_page():
    yt_id = database.get_active_idle_video()
    if yt_id:
        return render_template("idle.html", yt_id=yt_id)
    return redirect(url_for("kiosk_bp.home"))

@kiosk_bp.route("/faculties")
def faculties_page():
    return render_template("faculties.html")

@kiosk_bp.route("/video")
def video_page():
    faculty = request.args.get("faculty")
    return render_template("video.html", faculty=faculty)

@kiosk_bp.route("/schedule")
def schedule_page():
    return render_template("schedule.html")