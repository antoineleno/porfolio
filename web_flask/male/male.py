#!/usr/bin/python3
"""Male module"""
from male import app_views_male
from flask import render_template



@app_views_male.route("admin/dashboard/male", methods=["GET"])
def male():
    """Male views"""
    return render_template("male_buildings.html")

@app_views_male.route("admin/dashboard/display_male_building", methods=["GET"])
def display_male_blocks():
    """Display building"""
    return render_template("display_male_building.html")

@app_views_male.route("admin/dashboard/male_open_new_block", methods=["GET"])
def open_new_male_block():
    """Open a male new block"""
    return render_template("male_new_block.html")

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

