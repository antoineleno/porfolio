#!/usr/bin/python3
"""report module"""
from report import app_views_report
from flask import render_template



@app_views_report.route("/dashboard/report", methods=["GET"])
def report():
    """HOstle report views"""
    return render_template("hostel_report.html")
