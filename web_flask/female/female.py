#!/usr/bin/python3
"""female module"""
from female import app_views_female
from flask import render_template, url_for,  request
from models import storage



@app_views_female.route("admin/dashboard/female", methods=["GET"])
def female():
    """Female views"""
    zone_count = storage.count_zones(2)
    student_count = storage.count_students(2, 2)
    
    names = storage.all_block_name(2)
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

    return render_template("female_buildings.html", blocks = blocks)


@app_views_female.route("admin/dashboard/display_female_building", methods=["GET"])
def display_female_blocks():
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
    return render_template("display_female_building.html", block_name = block_name, residents=residents)






@app_views_female.route("admin/dashboard/female_open_new_block", methods=["GET"])
def open_new_female_block():
    """Open a male new block"""
    return render_template("female_new_block.html")

@app_views_female.route("admin/dashboard/female_insertion", methods=["GET"])
def insert_female():
    """Insert a  male student"""
    return render_template("female_insertion.html")

@app_views_female.route("admin/dashboard/female_manuel_insertion", methods=["GET"])
def insert_female_mamuelly():
    """Insert a  male student manuelly"""
    return render_template("female_manuel_insertion.html")


@app_views_female.route("admin/dashboard/female_bach_insert", methods=["GET"])
def batch_insert():
    """Insert a  batch of student"""
    return render_template("female_bach_insert.html")

@app_views_female.route("admin/dashboard/female_move_student", methods=["GET"])
def move_student():
    """Move a student"""
    return render_template("male_move_student.html")

@app_views_female.route("admin/dashboard/female_move_student", methods=["GET"])
def move_all_student():
    """Move all student"""
    return render_template("female_move_all_student.html")

@app_views_female.route("admin/dashboard/female_delete_student", methods=["GET"])
def delete_student():
    """Delete Student"""
    return render_template("female_deletion.html")


@app_views_female.route("admin/dashboard/female_move_student", methods=["GET"])
def batch_deletion():
    """Delete a batch of Student"""
    return render_template("female_bach_deletion.html")

@app_views_female.route("admin/dashboard/female_delete_block", methods=["GET"])
def block_deletion():
    """Delete a batch of Student"""
    return render_template("female_bach_insert.html")

@app_views_female.route("admin/dashboard/delete_room", methods=["GET"])
def delete_room():
    """Delete a room"""
    return render_template("male_delete_room.html")

@app_views_female.route("admin/dashboard/delete_zone", methods=["GET"])
def delete_zone():
    """Delete a room"""
    return render_template("male_delete_zone.html")
