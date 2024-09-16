#!/usr/bin/python3
"""Search module"""
from search import app_views_search
from flask import render_template, flash, url_for, request, redirect
from flask_login import login_required, current_user
from models import storage


@login_required
@app_views_search.route("admin/dashboard/search", methods=["GET"])
def search():
    """Search views"""
    return render_template("search_menu.html")


@login_required
@app_views_search.route("admin/dashboard/search_room", methods=["GET", "POST"])
def search_room():
    """Search room"""
    if current_user.id == storage.get_first_user()[0]:
        admin_name = storage.get_admin_name()
        hostel_type = ""
        if request.method == "POST":
            room_number = request.form.get('room_number')
            result = storage.get_all_room_residents(room_number)

            if len(result) == 0:
                hostel_type = room_number
                return render_template("display_room.html",
                                       admin_name=admin_name,
                                       result=result,
                                       room_number="Not Found in the hostel",
                                       hostel_type="")
            else:
                if result[0][0] == 1:
                    hostel_type = "Male Hostel"
                else:
                    hostel_type = "Female Hostel"
                return render_template("display_room.html",
                                       admin_name=admin_name,
                                       result=result,
                                       room_number=room_number,
                                       hostel_type=hostel_type)
    return render_template("search_room.html")


@login_required
@app_views_search.route("admin/dashboard/search_student",
                        methods=["GET", "POST"])
def search_student():
    """Search views"""
    if current_user.id == storage.get_first_user()[0]:
        admin_name = storage.get_admin_name()
        if request.method == "POST":
            student_id = request.form.get('student_id')
            result = storage.get_search_student(student_id)
            if len(result) == 0:
                student_id = "None"
                hostel_type = "None"
                name = "None"
                room = "NOne"
                country = "None"
                zone = "None"
                return render_template('display_student.html',
                                       admin_name=admin_name,
                                       hostel_type=hostel_type,
                                       name=name,
                                       room=room,
                                       country=country,
                                       zone=zone,
                                       student_id=student_id)
            else:
                hostel_type = ""
                name = result[0][2]
                room = result[0][1]
                country = result[0][3]
                zone = result[0][4]
                if result[0][0] == 1:
                    hostel_type = "Male"
                else:
                    hostel_type = "Female"
                return render_template('display_student.html',
                                       admin_name=admin_name,
                                       hostel_type=hostel_type,
                                       name=name,
                                       room=room,
                                       country=country,
                                       zone=zone,
                                       student_id=student_id)

    return render_template("search_student.html")
