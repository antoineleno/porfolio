#!/usr/bin/python3

from dashborad import app_views
from flask import render_template



@app_views.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("index.html")
