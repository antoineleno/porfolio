#!/usr/bin/python3
"""Male module"""
from male import app_views_male
from flask import render_template, flash,url_for, request, redirect
from models import storage
import os


@app_views_male.route("admin/dashboard/male", methods=["GET"])
def male():
    """Male views"""
    zone_count = storage.count_zones(1)
    student_count = storage.count_students(1, 1)
    
    names = storage.all_block_name(1)
    blocks_students = {}
    for i in range(len(names)):
        data = [student_count[i], zone_count[i]]
        blocks_students[names[i]] = data

    blocks = []
    colors = ["blue", "red", "hey", "new", "read", "orange", "yellow", "green"]
    j = 0

    for block_name in blocks_students.keys():
        occupancy = "{}/{}".format(blocks_students[block_name][0], blocks_students[block_name][1])
        block_info = {"name": block_name, "color": colors[j], "occupancy": occupancy, "url": url_for('app_views_male.display_male_blocks')}
        blocks.append(block_info)
        if j == 7:
            j = 0
        j += 1

    return render_template("male_buildings.html", blocks = blocks)

@app_views_male.route("admin/dashboard/display_male_building", methods=["GET"])
def display_male_blocks():
    """Display building"""
    block_name = request.args.get('block_name')
    block_residents = storage.get_all_zones_residents(block_name)
    residents = []
    ('25H-4-14', None, None, None, 'C')
    for i in range(len(block_residents)):
        room_number = block_residents[i][0]
        s_name = block_residents[i][1]
        student_id = block_residents[i][2]
        country = block_residents[i][3]
        zone = block_residents[i][4]
        room = {"room_number": room_number, 
                "student_name": s_name if s_name is not None else "",
                "student_id": student_id if student_id is not None else "",
                "country": country if country is not None else "",
                "zone": zone}
        residents.append(room)









    return render_template("display_male_building.html",
                           block_name = block_name,
                           residents = residents)



@app_views_male.route("admin/dashboard/male_open_new_block", methods=["GET", "POST"])
def open_new_male_block():
    """Open a male new block"""
    if request.method == "POST":
        name = request.form.get("block_name")
        block_name = ""
        if " " in name:
            block_name = name.replace(' ', '_')
        else:
            block_names = name
    
        levels = request.form.get("levels")
        rooms = request.form.get("rooms")
        students = request.form.get("students")

        block_names = []
        for a in range(1, 3):
            block_names += storage.all_block_name(a)
        
        if block_name in block_names:
            message = "The block already exists in the hostel, pleace open a new block"
            flash(message, " warnings")
            return redirect(url_for('app_views_male.operation_result'))
        else:
            args = "Building hostel_id=1 block_name={} {} {} {}".format(block_name,
                                                                        levels,
                                                                        rooms,
                                                                        students)
            storage.create_a_new_object(args)
            total_rooms = int(levels) * int(rooms)
            total_zones = int(levels) * int(rooms) * int(students)

            message = """Block {} has been successfully opened.
            """.format(name)
            flash(message, "success")
            return redirect(url_for('app_views_male.operation_result'))
    else:
        return render_template("male_new_block.html")













@app_views_male.route("admin/dashboard/operation_result", methods=["GET"])
def operation_result():
    """Display the result of the operation"""
    return render_template("operation_result.html")

@app_views_male.route("admin/dashboard/male_insertion", methods=["GET"])
def insert_male():
    """Insert a  male student"""
    return render_template("male_insertion.html")

@app_views_male.route("admin/dashboard/male_manuel_insertion", methods=["GET"])
def insert_male_mamuelly():
    """Insert a  male student manuelly"""
    return render_template("male_manuel_insertion.html")


@app_views_male.route("admin/dashboard/male_bach_insert", methods=["GET"])
def batch_insert():
    """Insert a  batch of student"""
    return render_template("male_bach_insert.html")

@app_views_male.route("admin/dashboard/male_move_student", methods=["GET"])
def move_student():
    """Move a student"""
    return render_template("male_move_student.html")

@app_views_male.route("admin/dashboard/male_move_student", methods=["GET"])
def move_all_student():
    """Move all student"""
    return render_template("male_move_all_student.html")

@app_views_male.route("admin/dashboard/male_delete_student", methods=["GET"])
def delete_student():
    """Delete Student"""
    return render_template("male_deletion.html")


@app_views_male.route("admin/dashboard/male_move_student", methods=["GET"])
def batch_deletion():
    """Delete a batch of Student"""
    return render_template("male_bach_deletion.html")

@app_views_male.route("admin/dashboard/male_delete_block", methods=["GET"])
def block_deletion():
    """Delete a batch of Student"""
    return render_template("male_bach_deletion.html")

@app_views_male.route("admin/dashboard/delete_room", methods=["GET"])
def delete_room():
    """Delete a room"""
    return render_template("male_delete_room.html")

@app_views_male.route("admin/dashboard/delete_zone", methods=["GET"])
def delete_zone():
    """Delete a room"""
    return render_template("male_delete_zone.html")

