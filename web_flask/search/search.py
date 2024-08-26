#!/usr/bin/python3
"""Search module"""
from search import app_views_search
from flask import render_template



@app_views_search.route("admin/dashboard/search", methods=["GET"])
def search():
    """Search views"""
    return render_template("search_menu.html")

@app_views_search.route("admin/dashboard/search_room", methods=["GET"])
def search_room():
    """Search room"""
    return render_template("search_room.html")

@app_views_search.route("admin/dashboard/search_student", methods=["GET"])
def search_student():
    """Search views"""
    return render_template("search_student.html")