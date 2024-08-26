#!/usr/bin/python3
"""leaves module"""
from leaves import app_views_leaves
from flask import render_template



@app_views_leaves.route("admin/dashboard/leaves", methods=["GET"])
def leaves():
    """Hostel leaves views"""
    return render_template("hostel_leaves.html")


@app_views_leaves.route("admin/dashboard/on_leave_students", methods=["GET"])
def on_leave_student():
    """On leaves  views"""
    return render_template("on_leave_students.html")

@app_views_leaves.route("admin/dashboard/overstay_students", methods=["GET"])
def over_stay_students():
    """Overstay student views"""
    return render_template("overstay.html")