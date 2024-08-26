#!/usr/bin/python3
"""female module"""
from female import app_views_female
from flask import render_template



@app_views_female.route("admin/dashboard/female", methods=["GET"])
def female():
    """Female views"""
    return render_template("female_buildings.html")


@app_views_female.route("admin/dashboard/display_female_building", methods=["GET"])
def display_male_blocks():
    """Display building"""
    return render_template("display_female_building.html")

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
