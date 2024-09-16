#!/usr/bin/python3
"""dashboard module"""
from dashboard import app_views_dashboard
from flask import render_template, flash, request, redirect, url_for
import models
from flask import jsonify
from models.base_model import BaseModel
from models.hostel import Hostel
from models.building import Building
from models.leave_request import Leave
from models.student import Student
from models import storage
from flask_login import login_required, current_user
from models.school import School


@app_views_dashboard.route("admin/dashboard", methods=["GET"])
@login_required
def dashboard():
    """Dashboard Views"""

    if current_user.id == storage.get_first_user()[0]:
        male_blocks = storage.count_block(1)
        male_students = storage.count_students(1)
        female_blocks = storage.count_block(2)
        female_students = storage.count_students(2)
        applicants = storage.get_application("application")
        admin_name = storage.get_admin_name()
        new_applicants = storage.get_application("inquiry")

        notifications = []
        for i in range(len(applicants)):
            new = {}
            name = applicants[i][0] + " made an application"
            times = applicants[i][1]
            new = {'name': name, 'time': storage.time_since(str(times))}
            notifications.append(new)

        inquiries = []
        for i in range(len(new_applicants)):
            new = {}
            name = new_applicants[i][0] + " made an Inquiry"
            times = new_applicants[i][1]
            new = {'name': name, 'time': storage.time_since(str(times))}
            inquiries.append(new)

        applications = []
        for j in range(len(applicants)):
            message = {}
            name = applicants[j][0]
            time = applicants[j][1]
            message = {'name': name, 'time': storage.time_since(str(time)),
                       'application_text': 'New application...'}
            applications.append(message)

        inquiries_goes = []
        for j in range(len(new_applicants)):
            message = {}
            name = new_applicants[j][0]
            time = new_applicants[j][1]
            message = {'name': name, 'time': storage.time_since(str(time)),
                       'inquiry_text': 'New Inquiry...'}
            inquiries_goes.append(message)

        return render_template("index.html", male_blocks=male_blocks,
                               male_students=male_students,
                               female_blocks=female_blocks,
                               female_students=female_students,
                               notifications=notifications,
                               inquiries=inquiries,
                               applications=applications,
                               inquiries_goes=inquiries_goes,
                               admin_name=admin_name)
    else:
        return render_template("404.html")


@app_views_dashboard.route('/api/chart-data')
def chart_data():
    """API call for both male and female chart data"""
    male_block_names = [name for name in storage.all_block_name(1)]
    male_data = {
        "labels": [block_name for block_name in male_block_names],
        "values": storage.count_students(1, 1)
        }

    female_block_names = [name for name in storage.all_block_name(2)]
    female_data = {
        "labels": [name for name in female_block_names],
        "values": storage.count_students(2, 2)
        }

    data = {
        "male": male_data,
        "female": female_data
        }

    return jsonify(data)


@app_views_dashboard.route("admin/setting/delete", methods=["GET", "POST"])
@login_required
def delete():
    """delete a row of school"""
    if request.method == "POST":
        delete_id = request.form.get('delete_id')
        if delete_id:
            storage.delete_school(delete_id)
            return redirect(url_for('app_views_dashboard.setting'))
    else:
        return redirect(url_for('app_views_dashboard.setting'))


@app_views_dashboard.route("admin/setting", methods=["GET", "POST"])
@login_required
def setting():
    """School administrator update"""

    if request.method == "POST":
        new_school = request.form.getlist('new_school[]')
        new_dean = request.form.getlist('new_dean[]')
        new_email = request.form.getlist('new_email[]')

        if (new_school and new_dean and new_email and
                new_school[0] and new_dean[0] and new_email[0]):

            school_exits = storage.check_school_existence()
            if new_school[0].upper() in school_exits:
                message = "The School exist aleady please add a new school"
                flash(message, "warning")
                my_url = "app_views_dashboard.setting"
                return redirect(url_for(my_url))

            school = new_school[0]
            if " " in new_school[0]:
                school = new_school[0].replace(" ", "_")
            dean = new_dean[0]
            if " " in new_dean[0]:
                dean = new_dean[0].replace(" ", "_")
            email = new_email[0]
            if " " in new_email[0]:
                email = new_email[0].replace(" ", "_")

            args = "School school_name={} school_dean={} email={}".format(
                school.upper(), dean, email)
            storage.create_a_new_object(args)
            return redirect(url_for('app_views_dashboard.setting'))

        else:
            return redirect(url_for('app_views_dashboard.delete'))
    else:
        school_admings = storage.get_school_list()
        admins = []
        for i in range(len(school_admings)):
            value = {"id": school_admings[i][0],
                     "school": school_admings[i][1],
                     "dean": school_admings[i][2],
                     "email": school_admings[i][3]}
            admins.append(value)

        return render_template('setting.html', admins=admins)
