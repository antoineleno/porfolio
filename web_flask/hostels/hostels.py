#!/usr/bin/python3
"""Male module"""
from hostels import app_views_male
from hostels import app_views_female
from flask import render_template, flash, url_for, request, redirect
from models import storage
from flask_login import login_required, current_user
from models import storage
import os
import shlex
import pycountry
import csv
import io


@app_views_female.route("/admin/dashboard/female", methods=["GET"])
@app_views_male.route("/admin/dashboard/male", methods=["GET"])
@login_required
def buildings():
    """buildings views"""
    if request.method == "GET":
        n = 0
        hostel_type = ""
        if request.path == "/campusstay/admin/dashboard/male":
            n = 1
            hostel_type = "Male Hostel"
        elif request.path == "/campusstay/admin/dashboard/female":
            n = 2
            hostel_type = "Female Hostel"
        admin_name = storage.get_admin_name()
        zone_count = storage.count_zones(n)
        student_count = storage.count_students(n, n)

        names = storage.all_block_name(n)
        blocks_students = {}
        for i in range(len(names)):
            data = [student_count[i], zone_count[i]]
            blocks_students[names[i]] = data

        blocks = []
        colors = ["blue", "red", "hey", "new", "read",
                  "orange", "yellow", "green"
                  ]
        j = 0

        for block_name in blocks_students.keys():
            occupancy = "{}/{}".format(blocks_students[block_name][0],
                                       blocks_students[block_name][1])
            my_url = "app_views_{}.display_blocks".format(
                "male" if n == 1 else "female")
            block_info = {"name": block_name, "color": colors[j],
                          "occupancy": occupancy,
                          "url": url_for(my_url)}
            blocks.append(block_info)
            if j == 7:
                j = 0
            j += 1

        return render_template("buildings.html",
                               blocks=blocks,
                               admin_name=admin_name,
                               hostel_type=hostel_type)
    else:
        return render_template("404.html")


@app_views_male.route("admin/dashboard/display_male_building", methods=["GET"])
@app_views_female.route("admin/dashboard/display_female_building",
                        methods=["GET"])
@login_required
def display_blocks():
    """Display building"""
    f_path = "/campusstay/admin/dashboard/display_female_building"
    if current_user.id == storage.get_first_user()[0]:
        hostel_type = ""
        if request.path == "/campusstay/admin/dashboard/display_male_building":
            hostel_type = "Male Hostel"
        elif request.path == f_path:
            hostel_type = "Female Hostel"
        admin_name = storage.get_admin_name()
        block_name = request.args.get('block_name')
        block_residents = storage.get_all_zones_residents(block_name)

        residents = []
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
        display_heading = " Block : {}".format(block_name)
        return render_template("display_buildings.html",
                               display_heading=display_heading,
                               residents=residents,
                               admin_name=admin_name,
                               hostel_type=hostel_type)
    else:
        return render_template('404.html')


@app_views_male.route("/admin/dashboard/male_open_new_block",
                      methods=["GET", "POST"])
@app_views_female.route("/admin/dashboard/female_open_new_block",
                        methods=["GET", "POST"])
@login_required
def open_new_block():
    """Open a new block"""

    if current_user.id == storage.get_first_user()[0]:
        admin_name = storage.get_admin_name()
        hostel_type = ""
        H_name = ""
        hostel_type = "Male Hostel"
        n = 1
        H_name = "male"
        if request.path == "/campusstay/admin/dashboard/female_open_new_block":
            n = 2
            name = "female"
            hostel_type = "Female Hostel"

        if request.method == "POST":
            name = request.form.get("block_name")
            block_name = name

            if " " in name:
                block_name = name.replace(' ', '_')

            levels = request.form.get("levels")
            rooms = request.form.get("rooms")
            students = request.form.get("students")

            block_names = []
            for a in range(1, 3):
                block_names += storage.all_block_name(a)

            if block_name in block_names:
                message = """The block {} already exists in the
                hostel, pleace open a new .
                """.format(block_name)
                flash(message, "warning")
                my_url = "app_views_{}.operation_result".format(
                    "male" if hostel_type == "Male Hostel" else "female"
                )

                return redirect(url_for(my_url))
            else:
                args = """Building hostel_id={}
                    block_name={} {} {} {}""".format(n, block_name,
                                                     levels,
                                                     rooms,
                                                     students)
                storage.create_a_new_object(args)

                message = """Block {} has been successfully opened.
                """.format(name)
                flash(message, "success")
                f_url = "app_views_{}.operation_result".format(H_name)
                return redirect(url_for(f_url))
        else:
            return render_template("new_block.html",
                                   admin_name=admin_name,
                                   hostel_type=hostel_type)
    else:
        return render_template('404.html')


@app_views_male.route("admin/dashboard/male_insertion",
                      methods=["GET", "POST"])
@app_views_female.route("admin/dashboard/female_insertion",
                        methods=["GET", "POST"])
@login_required
def insert_student_randomlly():
    """Insert a  male student"""

    if current_user.id == storage.get_first_user()[0]:
        admin_name = storage.get_admin_name()
        hostel_type = ""
        message = ""
        H_name = ""
        r_type = ""
        hostel_type = "Male Hostel"
        n = 1
        H_name = "male"

        if request.path == "/campusstay/admin/dashboard/female_insertion":
            n = 2
            name = "female"
            hostel_type = "Female Hostel"

        if request.method == "POST":
            name = request.form.get("student_name").title()
            student_name = name
            if " " in name:
                student_name = name.replace(' ', '_')
            s_id = request.form.get("student_id")
            student_id = s_id
            if " " in s_id:
                student_id = s_id.replace(' ', '_')
            country_code = request.form.get("country")
            s_country = pycountry.countries.get(alpha_2=country_code).name
            country = s_country
            if " " in s_country:
                country = s_country.replace(' ', '_')

            args = "{} {} {} {}".format(n, student_name, student_id, country)
            arguments = shlex.split(args)

            Hostels = []
            Room_ID = []

            Hostels = storage.all_block_name(n)
            found = False
            for j in range(len(Hostels)):
                Room_ID += storage.all_room_id(Hostels[j])
                for i in range(len(Room_ID)):
                    answer = storage.insert_student(arguments[1],
                                                    arguments[2],
                                                    arguments[3].title(),
                                                    Room_ID[i])
                    if isinstance(answer, list):
                        message = """Student Insert in Room : {}
                        Zone  {}""".format(
                            answer[0][0], answer[0][1])
                        r_type = "success"
                        user_name = answer[0][0] + "-{}".format(answer[0][1])
                        new_user = """User full_name={} username={}
                        password={}
                        """.format(student_name.title(),
                                   user_name, student_id)

                        storage.create_a_new_object(new_user)
                        storage.get_user_id_update_student(user_name,
                                                           student_id)
                        found = True
                        break
                    elif answer == 404:
                        message = """The student with ID {} already exists
                        in the hostel""".format(arguments[2])
                        r_type = "warning"
                        found = True
                        break
                if found is True:
                    break
            if message == "":
                message = """No place found for {} Insert him manuelly
                    or open a new building for him!""".format(arguments[2])
                r_type = "warning"

            flash(message, r_type)
            f_url = "app_views_{}.operation_result".format(H_name)
            return redirect(url_for(f_url))

        return render_template("insertion.html", admin_name=admin_name,
                               hostel_type=hostel_type)
    else:
        return render_template('404.html')


@app_views_male.route("admin/dashboard/male_manuel_insertion",
                      methods=["GET", "POST"])
@app_views_female.route("admin/dashboard/female_manuel_insertion",
                        methods=["GET", "POST"])
@login_required
def insert_student_manuelly():
    """Insert a student manuelly"""
    if current_user.id == storage.get_first_user()[0]:
        admin_name = storage.get_admin_name()
        hostel_type = ""
        message = ""
        H_name = ""
        r_type = ""
        f_path = "/campusstay/admin/dashboard/female_manuel_insertion"
        hostel_type = "Male Hostel"
        n = 1
        H_name = "male"
        if request.path == f_path:
            n = 2
            name = "female"
            hostel_type = "Female Hostel"

        if request.method == "POST":

            name = request.form.get("student_name").title()
            s_id = request.form.get("student_id")
            s_room = request.form.get("room_number")
            s_zone = request.form.get("room_zone")
            country_code = request.form.get("country")
            s_country = pycountry.countries.get(alpha_2=country_code).name
            message, r_type = insertion_helper(name, s_id,
                                               s_country,
                                               s_room,
                                               s_zone)
            flash(message, r_type)
            f_url = "app_views_{}.operation_result".format(H_name)
            return redirect(url_for(f_url))
        return render_template("student_manuel_insertion.html",
                               admin_name=admin_name,
                               hostel_type=hostel_type)
    else:
        return render_template('404.html')


@app_views_male.route("admin/dashboard/male_batch_insert",
                      methods=["GET", "POST"])
@app_views_female.route("admin/dashboard/female_batch_insert",
                        methods=["GET", "POST"])
@login_required
def batch_insert():
    """Insert a  batch of student"""

    if current_user.id == storage.get_first_user()[0]:
        admin_name = storage.get_admin_name()
        hostel_type = ""
        message = ""
        H_name = ""
        r_type = ""
        hostel_type = "Male Hostel"
        n = 1
        H_name = "male"
        if request.path == "/campusstay/admin/dashboard/female_batch_insert":
            n = 2
            hostel_type = "Female Hostel"

        if request.method == "POST":
            try:
                file_name = request.files['csvFile']
                all_students = []
                byte_stream = file_name.stream.read()
                text_stream = io.StringIO(byte_stream.decode('utf-8'))
            except UnicodeDecodeError:
                message = "File wrong format"
                r_type = "warning"
                flash(message, r_type)
                f_url = "app_views_{}.operation_result".format(H_name)
                return redirect(url_for(f_url))

            inserted_students = []
            uninserted_students = []
            value = {}

            reader = csv.reader(text_stream)
            for row in reader:
                all_students.append(row)

            if len(all_students[0]) != 3:
                message = """Incorrect number of column, the file should
                only have three column
                """
                r_type = "warning"
                flash(message, r_type)
                f_url = "app_views_{}.operation_result".format(H_name)
                return redirect(url_for(f_url))

            elif (all_students[0][0].title() != "Name" or
                  all_students[0][1].upper() != "ID" or
                  all_students[0][2].title() != "Country"):

                message = """The values of the first row are incorrect make
                sure to respect the format indicated"""
                r_type = "warning"
                flash(message, r_type)
                f_url = "app_views_{}.operation_result".format(H_name)
                return redirect(url_for(f_url))
            else:
                del all_students[0]
                for i in range(len(all_students)):
                    s_name = all_students[i][0]
                    if " " in all_students[i][0]:
                        s_name = all_students[i][0].replace(" ", "_")

                    s_id = all_students[i][1]
                    if " " in all_students[i][1]:
                        s_id = all_students[i][1].replace(" ", "_")

                    s_country = all_students[i][2]
                    if " " in all_students[i][2]:
                        s_country = all_students[i][2].replace(" ", "_")

                    new_argument = (str(n) +
                                    " " + s_name +
                                    " " + s_id +
                                    " " + s_country)
                    arguments = shlex.split(new_argument)
                    Hostels = []
                    Room_ID = []
                    Hostels = storage.all_block_name(n)
                    if len(Hostels) == 0:
                        v_v = """No place found, insert him manuelly or
                                open a new block
                            """
                        value = {"ID": s_id, "Description": v_v}
                        uninserted_students.append(value)
                    found = False
                    for j in range(len(Hostels)):
                        Room_ID += storage.all_room_id(Hostels[j])
                        a_name = arguments[3].title()
                        for k in range(len(Room_ID)):
                            answer = storage.insert_student(arguments[1],
                                                            arguments[2],
                                                            a_name,
                                                            Room_ID[k])
                            if isinstance(answer, list):
                                value = {"ID": s_id, "Room": answer[0][0],
                                         "Zoom": answer[0][1]}
                                inserted_students.append(value)
                                found = True
                                new_user = """User full_name={} username={}
                                password={}""".format(s_name.title(),
                                                      answer[0][0], s_id)
                                storage.create_a_new_object(new_user)
                                storage.get_user_id_update_student(
                                    answer[0][0], s_id)
                                break
                            elif answer == 404:
                                value = {"ID": s_id, "Description":
                                         """The student already
                                         exist in the hostel"""}
                                uninserted_students.append(value)
                                found = True
                                break
                        if found is True:
                            break
                        value = {"ID": s_id, "Description":
                                 """No place found, insert him manuelly or
                                 open a new block"""}
                        uninserted_students.append(value)

            message = {"Inserted_student": inserted_students,
                       "Uninserted_student": uninserted_students}
            flash(message)
            f_url = "app_views_{}.batch_insertion_result".format(H_name)
            return redirect(url_for(f_url))
        return render_template("bach_insert.html", admin_name=admin_name,
                               hostel_type=hostel_type)
    else:
        return render_template('404.html')


@app_views_male.route("admin/dashboard/male_move_student",
                      methods=["GET", "POST"])
@app_views_female.route("admin/dashboard/female_move_student",
                        methods=["GET", "POST"])
@login_required
def move_student():
    """Move a student"""

    if current_user.id == storage.get_first_user()[0]:
        admin_name = storage.get_admin_name()
        hostel_type = ""
        message = ""
        H_name = ""
        r_type = ""
        f_path = "/campusstay/admin/dashboard/female_move_student"
        hostel_type = "Male Hostel"
        H_name = "male"
        if request.path == f_path:
            name = "female"
            hostel_type = "Female Hostel"

        if request.method == "POST":

            s_id = request.form.get("student_id")
            student_id = s_id
            if " " in s_id:
                student_id = s_id.replace(' ', '_')
            s_room = request.form.get("room_number")
            room = s_room
            if " " in s_room:
                room = s_room.replace(" ", "_")
            s_zone = request.form.get("room_zone")
            zone = s_zone
            if " " in s_zone:
                zone = s_zone.replace(" ", "_")

            user_id = storage.get_user_id_from_students(s_id)
            student_full_infos = storage.get_student_infos_before(s_id)

            if len(student_full_infos) == 0:
                message = "The studen does not exist in the hostel"
                r_type = "warning"
                flash(message, r_type)
                f_url = "app_views_{}.operation_result".format(H_name)
                return redirect(url_for(f_url))

            else:
                answer = storage.object_to_delete("student", s_id)
                storage.delete_user(user_id[0])
                name = student_full_infos[0][0]

                s_country = student_full_infos[0][1]
                message, r_type = insertion_helper(name, s_id,
                                                   s_country,
                                                   s_room,
                                                   s_zone)
                flash(message, r_type)
                f_url = "app_views_{}.operation_result".format(H_name)
                return redirect(url_for(f_url))
        return render_template("move_student.html",
                               admin_name=admin_name,
                               hostel_type=hostel_type)
    else:
        return render_template('404.html')


@app_views_male.route("admin/dashboard/male_move_student", methods=["GET"])
@login_required
def move_all_student():
    """Move all student"""

    if current_user.id == storage.get_first_user()[0]:
        return render_template("male_move_all_student.html")
    else:
        return render_template('404.html')


@app_views_male.route("admin/dashboard/male_delete_student",
                      methods=["GET", "POST"])
@app_views_female.route("admin/dashboard/female_delete_student",
                        methods=["GET", "POST"])
@login_required
def delete_student():
    """Delete Student"""

    if current_user.id == storage.get_first_user()[0]:
        admin_name = storage.get_admin_name()
        hostel_type = ""
        message = ""
        H_name = ""
        r_type = ""
        f_path = "/campusstay/admin/dashboard/female_delete_student"
        hostel_type = "Male Hostel"
        H_name = "male"
        if request.path == f_path:
            H_name = "female"
            hostel_type = "Female Hostel"

        if request.method == "POST":
            s_id = request.form.get("student_id")
            user_id = storage.get_user_id_from_students(s_id)
            storage.delete_all_student_leaves(s_id)
            answer = storage.object_to_delete("student", s_id)

            if answer == - 1:
                message = "The student does not exist"
                r_type = "warning"
            else:
                storage.delete_user(user_id[0])
                message = "Student {} deleted successfully".format(s_id)
                r_type = "success"

            flash(message, r_type)
            f_url = "app_views_{}.operation_result".format(H_name)
            return redirect(url_for(f_url))
        else:
            return render_template('student_deletion.html',
                                   admin_name=admin_name,
                                   hostel_type=hostel_type)


@app_views_male.route("admin/dashboard/male_batch_deletion",
                      methods=["GET", "POST"])
@app_views_female.route("admin/dashboard/female_batch_deletion",
                        methods=["GET", "POST"])
@login_required
def batch_deletion():
    """Delete a batch of Student"""

    if current_user.id == storage.get_first_user()[0]:
        admin_name = storage.get_admin_name()
        hostel_type = ""
        message = ""
        H_name = ""
        r_type = ""
        hostel_type = "Male Hostel"
        n = 1
        H_name = "male"

        if request.path == "/campusstay/admin/dashboard/female_batch_deletion":
            n = 2
            hostel_type = "Female Hostel"

        if request.method == "POST":
            try:
                file_name = request.files['csvFile']
                all_students = []
                byte_stream = file_name.stream.read()
                text_stream = io.StringIO(byte_stream.decode('utf-8'))
            except UnicodeDecodeError:
                message = "File wrong format"
                r_type = "warning"
                flash(message, r_type)
                f_url = "app_views_{}.operation_result".format(H_name)
                return redirect(url_for(f_url))

            deleted_students = []
            undeleted_students = []
            value = {}

            reader = csv.reader(text_stream)
            for row in reader:
                all_students.append(row)

            if len(all_students[0]) != 1:
                message = """Incorrect number of column, the file can
                only have one column
                """
                r_type = "warning"
                flash(message, r_type)
                f_url = "app_views_{}.operation_result".format(H_name)
                return redirect(url_for(f_url))

            elif (all_students[0][0].upper() != "ID"):
                message = """The values of the first row are incorrect make
                sure to respect the format indicated"""
                r_type = "warning"
                flash(message, r_type)
                f_url = "app_views_{}.operation_result".format(H_name)
                return redirect(url_for(f_url))
            else:
                del all_students[0]
                for i in range(len(all_students)):
                    s_id = all_students[i][0]
                    if " " in all_students[i][0]:
                        s_id = all_students[i][0].replace(" ", "_")

                    answer = storage.object_to_delete("student", s_id)
                    if answer == - 1:
                        mess = "The student does not exist"
                        value = {"ID": s_id, "Description": mess}
                        undeleted_students.append(value)
                    else:
                        mess = "Student successfully deleted"
                        value = {"ID": s_id, "Description": mess}
                        deleted_students.append(value)
            message = {"deleted_student": deleted_students,
                       "Undeleted_student": undeleted_students}

            flash(message)
            f_url = "app_views_{}.batch_deletion_result".format(H_name)
            return redirect(url_for(f_url))
        return render_template("batch_deletion.html", admin_name=admin_name,
                               hostel_type=hostel_type)
    else:
        return render_template('404.html')


@app_views_male.route("admin/dashboard/male_delete_block",
                      methods=["GET", "POST"])
@app_views_female.route("admin/dashboard/female_delete_block",
                        methods=["GET", "POST"])
@login_required
def delete_block():
    """Delete a block"""

    if current_user.id == storage.get_first_user()[0]:
        admin_name = storage.get_admin_name()
        hostel_type = ""
        message = ""
        H_name = ""
        r_type = ""
        f_path = "/campusstay/admin/dashboard/female_delete_block"
        hostel_type = "Male Hostel"

        H_name = "male"
        if request.path == f_path:
            H_name = "female"
            hostel_type = "Female Hostel"

        if request.method == "POST":
            block_name = request.form.get("block_name")
            answer = storage.object_to_delete("block", block_name)

            if answer == - 1:
                message = """There are students in this building
                move them first"""
                r_type = "warning"
            elif answer == 1:
                message = """{} deleted successfully""".format(block_name)
                r_type = "success"
            else:
                message = "Block {} does not exist".format(block_name)
                r_type = "warning"

            flash(message, r_type)
            f_url = "app_views_{}.operation_result".format(H_name)
            return redirect(url_for(f_url))
        else:
            return render_template('delete_block.html', admin_name=admin_name,
                                   hostel_type=hostel_type)


@app_views_male.route("admin/dashboard/male_delete_room",
                      methods=["GET", "POst"])
@app_views_female.route("admin/dashboard/female_delete_room",
                        methods=["GET", "POst"])
@login_required
def delete_room():
    """Delete a room"""

    if current_user.id == storage.get_first_user()[0]:
        admin_name = storage.get_admin_name()
        hostel_type = ""
        message = ""
        H_name = ""
        r_type = ""
        f_path = "/campusstay/admin/dashboard/female_delete_room"
        hostel_type = "Male Hostel"

        H_name = "male"
        if request.path == f_path:
            H_name = "female"
            hostel_type = "Female Hostel"

        if request.method == "POST":
            room_number = request.form.get("room_number")
            answer = storage.object_to_delete('room', room_number)
            if answer == -1:
                message = """There are students in this room, can't remove it
                move students first"""
                r_type = "warning"
            elif answer == 1:
                message = "Room {} Successfully deleted".format(room_number)
                r_type = "success"
            else:
                message = "The room does not exist"
                r_type = "warning"

            flash(message, r_type)
            f_url = "app_views_{}.operation_result".format(H_name)
            return redirect(url_for(f_url))
        else:
            return render_template('delete_room.html', admin_name=admin_name,
                                   hostel_type=hostel_type)


@app_views_male.route("admin/dashboard/male_delete_zone",
                      methods=["GET", "POST"])
@app_views_female.route("admin/dashboard/female_delete_zone",
                        methods=["GET", "POST"])
@login_required
def delete_zone():
    """Delete a zone"""

    if current_user.id == storage.get_first_user()[0]:
        admin_name = storage.get_admin_name()
        hostel_type = ""
        message = ""
        H_name = ""
        r_type = ""
        f_path = "/campusstay/admin/dashboard/female_delete_zone"
        hostel_type = "Male Hostel"

        H_name = "male"
        if request.path == f_path:
            H_name = "female"
            hostel_type = "Female Hostel"

        if request.method == "POST":

            room_number = request.form.get("room_number")
            zone = request.form.get("zone")
            answer = storage.object_to_delete("zone",
                                              zone.upper(),
                                              room_number)

            if answer == -1:
                message = """There is a student living in this zone
                move him first before deleting the zone"""
                r_type = "warning"
            elif answer == 1:
                message = "Room {} Zone {} Successfully deleted".format(
                    room_number, zone)
                r_type = "success"
            else:
                message = "The zone does not exist"
                r_type = "warning"

            flash(message, r_type)
            f_url = "app_views_{}.operation_result".format(H_name)
            return redirect(url_for(f_url))
        else:
            return render_template('delete_zone.html', admin_name=admin_name,
                                   hostel_type=hostel_type)


def insertion_helper(name, s_id, s_country, s_room, s_zone):
    """Helper function to insert student maneuelly"""
    message = ""
    r_type = ""
    student_name = name
    if " " in name:
        student_name = name.replace(' ', '_')
    s_id = request.form.get("student_id")
    student_id = s_id
    if " " in s_id:
        student_id = s_id.replace(' ', '_')

    country = s_country
    if " " in s_country:
        country = s_country.replace(' ', '_')

    room = s_room
    if " " in s_room:
        room = s_room.replace(" ", "_")

    zone = s_zone
    if " " in s_zone:
        zone = s_zone.replace(" ", "_")
    all_rooms = storage.get_all_rooms()
    hostel_rooms = [room[0] for room in all_rooms]
    room_zones = storage.get_all_zones(room)
    hostel_zones = [z[0] for z in room_zones]

    if room not in hostel_rooms or zone.upper() not in hostel_zones:
        message = """Room {} or Zone {} does't exist
        in the hostel.""".format(room, zone)
        r_type = "warning"
        return message, r_type

    args = "{} {} {} {} {}".format(student_name,
                                   student_id,
                                   country,
                                   zone.upper(),
                                   room)
    arguments = shlex.split(args)
    answer = storage.insert_student(
        arguments[0],
        arguments[1].title(),
        arguments[2],
        arguments[3].upper(),
        arguments[4])

    if answer == 2:
        message = "Student insert in room {} Zone {}".format(room,
                                                             zone.upper())
        r_type = "success"
        new_user = """User full_name={} username={}
        password={}""".format(student_name.title(),
                              room, student_id)
        storage.create_a_new_object(new_user)
        storage.get_user_id_update_student(room, student_id)
    elif answer == 1:
        message = "The Student already exist in the Building."
        r_type = "warning"
    else:
        message = "A student already exist in this zone."
        r_type = "warning"
    return (message, r_type)


@app_views_male.route("admin/dashboard/operation_result", methods=["GET"])
@app_views_female.route("admin/dashboard/operation_result", methods=["GET"])
@login_required
def operation_result():
    """Display the result of the operation"""

    if current_user.id == storage.get_first_user()[0]:
        admin_name = storage.get_admin_name()
        return render_template("operation_result.html", admin_name=admin_name)
    else:
        return render_template('404.html')


@app_views_male.route("admin/dashboard/batch_insertion_result",
                      methods=["GET"])
@app_views_female.route("admin/dashboard/batch_insertion_result",
                        methods=["GET"])
@login_required
def batch_insertion_result():
    """Display the result of the operation"""

    if current_user.id == storage.get_first_user()[0]:
        admin_name = storage.get_admin_name()
        return render_template("display_bach_insertion_result.html",
                               admin_name=admin_name)
    else:
        return render_template('404.html')


@app_views_male.route("admin/dashboard/batch_deletion_result", methods=["GET"])
@app_views_female.route("admin/dashboard/batch_deletion_result",
                        methods=["GET"])
@login_required
def batch_deletion_result():
    """Display the result of the operation"""

    if current_user.id == storage.get_first_user()[0]:
        admin_name = storage.get_admin_name()
        return render_template("display_bach_deletion_result.html",
                               admin_name=admin_name)
    else:
        return render_template('404.html')
