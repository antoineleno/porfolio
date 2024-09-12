#!/usr/bin/python3
"""dashboard module"""
from user import app_views_user
from flask import render_template, request, url_for, redirect, flash
from user import app_views_user
from flask_login import login_required, current_user
from models import storage
import os
from werkzeug.utils import secure_filename
from PIL import Image
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


@app_views_user.route("user/home", methods=["GET"])
@login_required
def home():
    """Dashboard Views"""

    file_path = "./dashboard/static/img/{}.png".format(current_user.id)

    if os.path.exists(file_path):
        profile_path = current_user.id
    else:
        profile_path = "man"

    result = storage.get_all_user_infos(current_user.id)
    room_number = result[0][0]
    room_capacity = storage.get_room_capacity(room_number)
    Student_name = result[0][1]
    Student_id = result[0][2]
    room_zone = result[0][3]
    email = current_user.email
    school = current_user.department

    profiles = []
    roommates = storage.user_roommates(current_user.id)

    for i in range(len(roommates)):
        file_path = "./dashboard/static/img/{}.png".format(roommates[i][1])
        if roommates[i][1] != current_user.id:
            if os.path.exists(file_path):
                mate_infos = {"name": roommates[i][0],
                              "profile_path": roommates[i][1]}
            else:
                mate_infos = {"name": roommates[i][0], "profile_path": "man"}
            profiles.append(mate_infos)

    return render_template('user_index.html',
                           room_number=room_number,
                           Student_name=Student_name,
                           Student_id=Student_id,
                           room_zone=room_zone,
                           email=email,
                           school=school,
                           profile_path=profile_path,
                           room_capacity=room_capacity,
                           profiles=profiles)


@app_views_user.route("user/profile", methods=["GET", "POST"])
@login_required
def user_profile():
    """Manage user profile"""
    file_path = "./dashboard/static/img/{}.png".format(current_user.id)

    if os.path.exists(file_path):
        profile_path = current_user.id
    else:
        profile_path = "man"

    result = storage.get_all_user_infos(current_user.id)
    room_number = result[0][0]
    Student_name = result[0][1]
    Student_id = result[0][2]
    email = current_user.email
    school = current_user.department
    username = current_user.username

    if request.method == "POST":
        message = ""
        r_type = ""
        new_email = request.form.get('email')
        new_school = request.form.get('new_school')
        new_username = request.form.get('username')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        file = request.files.get('profilePic')
        user_oject = storage.get_user_object(current_user.id)
        if new_email:
            user_oject.email = new_email
        if new_school:
            user_oject.department = new_school
        if new_username:
            user_oject.username = new_username

        storage.save()

        if 'profilePic' in request.files:
            file = request.files['profilePic']
            if file:
                a = get_image_dimensions(file)[0]
                b = get_image_dimensions(file)[1]

                if allowed_file(file.filename) and a == b:
                    filename = secure_filename(f"{current_user.id}.png")
                    file.save(os.path.join('dashboard', 'static', 'img',
                                           filename))
                    profile_path = filename
                else:
                    message = """Incorrect picture format,
                    format png, height = width"""
                    flash(message, "danger")
                    f_url = "app_views_user.user_profile"
                    return redirect(url_for(f_url))

        message = ""
        r_type = ""
        if current_password:
            if user_oject.verify_password(password=current_password):
                if not new_password:
                    message = """Password not updated you should
                    provide a new password"""
                    r_type = "danger"
                else:
                    user_oject.password = new_password
                    r_type = "success"
                    message = "Password updated successfully"
                storage.save()
                flash(message, r_type)
                f_url = "app_views_user.user_profile"
                return redirect(url_for(f_url))
            else:
                message = """Incorrect password,
                your password has not been updated"""
                flash(message, "danger")
                f_url = "app_views_user.user_profile"
                return redirect(url_for(f_url))
        else:
            return redirect(url_for("app_views_user.user_profile"))
    else:
        return render_template('user_profile.html',
                               profile_path=profile_path,
                               room_number=room_number,
                               Student_name=Student_name,
                               Student_id=Student_id,
                               email=email,
                               school=school,
                               username=username)


@app_views_user.route("user/leave", methods=["GET", "POST"])
@login_required
def user_leaves():
    """User leave application"""
    file_path = "./dashboard/static/img/{}.png".format(current_user.id)

    if os.path.exists(file_path):
        profile_path = current_user.id
    else:
        profile_path = "man"

    result = storage.get_all_user_infos(current_user.id)
    room_number = result[0][0]
    Student_name = result[0][1]
    Student_id = result[0][2]

    if request.method == "POST":
        reason = request.form.get('reason')
        place = request.form.get('place')
        Start_date = request.form.get('start_date')
        End_date = request.form.get('end_date')
        description = request.form.get('reason_description')

        student_id = storage.get_all_user_infos(current_user.id)[0][2]
        new_leaves = "Leave student_id={} start_date={} end_date={} place={} description={}".format(student_id,
                                                                                                    Start_date,
                                                                                                    End_date,
                                                                                                    place,
                                                                                                    reason,
                                                                                                    description)
        

        storage.create_a_new_object(new_leaves)
        leave_id = storage.get_leaves_object(student_id, Start_date, End_date, place)[0][0]
    
        mail_answer = send_application_to_school("lenoantoine2000@gmail.com", "LENO",
                                                 datetime.strptime(Start_date, '%Y-%m-%dT%H:%M').strftime('%d-%m-%Y'),
                                                 datetime.strptime(End_date, '%Y-%m-%dT%H:%M').strftime('%d-%m-%Y') ,
                                                 reason,
                                                 current_user.full_name, student_id, leave_id, "lenoantoine@gmail.com", description)
        message = ""
        r_type = ""
        if mail_answer == 1:
            message = """Your hostel leave application has been successfully submitted"""
            r_type = "success"
        else:
            message = """You hostel leave application has not been submitted"""
            r_type = "danger"

        flash(message, "success")
        f_url = "app_views_user.user_leaves"
        return redirect(url_for(f_url))



    return render_template('user_leaves.html', profile_path=profile_path,
                           room_number=room_number,
                           Student_name=Student_name,
                           Student_id=Student_id)


def allowed_file(filename):
    """Check file allow extention"""
    allowed_extensions = {'png'}
    ex = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and ex in allowed_extensions


def get_image_dimensions(file):
    """Check file dimeension"""
    file_copy = io.BytesIO(file.read())
    file.seek(0)

    img = Image.open(file_copy)
    return img.size


def send_application_to_school(receiver_email, dean_last_name, start_date, end_date, reason_for_leave, student_name, student_id, request_id, contact_info, r_description):
    """Send the leave application via mail"""
    email = "lenomadeleineantoine@gmail.com"
    subject = "Request for Hostel Leave"

    html_file_path = "user/templates/email_template.html"

    try:
        with open(html_file_path, 'r') as file:
            html_content = file.read()
    except FileNotFoundError:
        print(f"Error: The file {html_file_path} was not found.")
        return -1



    html_content = html_content.replace('[Dean\'s Last Name]', dean_last_name)
    html_content = html_content.replace('[Start Date]', start_date)
    html_content = html_content.replace('[End Date]', end_date)
    html_content = html_content.replace('[Reason for Leave]', reason_for_leave)
    html_content = html_content.replace('[Student Name]', student_name)
    html_content = html_content.replace('[Student ID]', student_id)
    html_content = html_content.replace('[Request ID]', request_id)
    html_content = html_content.replace('[Your Contact Information]', contact_info)
    html_content = html_content.replace('[Description]', r_description)



    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email, 'dwjo amny oeyf rvwi')
            server.sendmail(email, receiver_email, msg.as_string())
            return 1
    except Exception as e:
        print(f"Error: {e}")
        return -1





@app_views_user.route('/approve_leave')
def approve_leave():
    """Approve leave request"""
    request_id = request.args.get('request_id')
    message = ""
    response_type = ""
    if storage.check_leave_status(request_id):
        message = "Leave request already processed"
        response_type = "Proccessed"
    else:
        response_type = "approved"
        message ="Leave request has been successfully approved"
        storage.update_leave_school_response(request_id, True)
    return render_template('request_result.html', response_type=response_type,
                           message=message)

@app_views_user.route('/cancel_leave')
def cancel_leave():
    request_id = request.args.get('request_id')
    message = ""
    response_type = ""
    if storage.check_leave_status(request_id):
        message = "Leave request already processed"
        response_type = "Proccessed"
    else:
        response_type = "cancelled"
        message = "Leave request successfully cancelled"
        storage.update_leave_school_response(request_id, False)
    return render_template('request_result.html', response_type=response_type,
                           message = message)


