#!/usr/bin/python3
"""dashboard module"""
from dashboard import app_views_dashboard
from flask import render_template
import models
from flask import jsonify
from models.base_model import BaseModel
from models.hostel import Hostel
from models.building import Building
from models.leave_request import Leave
from models.student import Student
from models import storage
from flask_login import login_required, current_user


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


@app_views_dashboard.route("admin/setting", methods=["GET"])
@login_required
def setting():
    """Dashboard Views"""
    return render_template('setting.html')
