#!/usr/bin/python3
"""dashboard module"""
from dashboard import app_views_dashboard
from flask import render_template



@app_views_dashboard.route("admin/dashboard", methods=["GET"])
def dashboard():
    """Dashboard Views"""
    return render_template("index.html")
