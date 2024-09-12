#!/usr/bin/python3
"""inquiries module"""
from inquiries import app_views_inquiries
from flask import render_template



@app_views_inquiries.route("admin/dashboard/inquiries", methods=["GET"])
def inquiries():
    """Inquiries view"""
    return render_template("inquiries.html")
