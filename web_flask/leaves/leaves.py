#!/usr/bin/python3
"""leaves module"""
from leaves import app_views_leaves
from flask import render_template, request, flash, redirect, url_for
from models import storage
import datetime
from flask_login import login_required, current_user
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


@app_views_leaves.route("admin/dashboard/leaves", methods=["GET", "POST"])
@login_required
def leaves():
    """Hostel leaves views"""
    if current_user.id == storage.get_first_user()[0]:
        results = storage.get_leaves()
        admin_name = storage.get_admin_name()

        if request.method == 'POST':
            student_id = request.form.get('student_id')
            action = request.form.get('action')
            if student_id and action:
                s_e = storage.get_student_name_email_to_send_conf(student_id)
                leave_id = storage.get_latest_leave_id(student_id)
                if action == 'approve':
                    storage.update_leave_approval(student_id, True, leave_id)
                    flash(f'Student {student_id} leave approved.', 'success')
                    send_leave_confirmation_to_student(s_e[0][0],
                                                       s_e[0][1], "approved")
                elif action == 'cancel':
                    storage.update_leave_approval(student_id, False, leave_id)
                    flash(f'Student {student_id} leave cancelled.', 'warning')
                    send_leave_confirmation_to_student(s_e[0][0],
                                                       s_e[0][1], "cancelled")
                else:
                    flash('Invalid action.', 'danger')

            return redirect(url_for('app_views_leaves.leaves'))
        return render_template("hostel_leaves.html",
                               results=results,
                               admin_name=admin_name)


@login_required
@app_views_leaves.route("admin/dashboard/on_leave_students", methods=["GET"])
def on_leave_student():
    """On leaves  views"""
    if current_user.id == storage.get_first_user()[0]:
        results = storage.get_on_leave_student()
        admin_name = storage.get_admin_name()
        return render_template("on_leave_students.html",
                               results=results,
                               admin_name=admin_name)


@login_required
@app_views_leaves.route("admin/dashboard/overstay_students", methods=["GET"])
def over_stay_students():
    """Overstay student views"""
    if current_user.id == storage.get_first_user()[0]:
        admin_name = storage.get_admin_name()
        results = storage.get_over_stay_students()
        return render_template("overstay.html", admin_name=admin_name,
                               results=results)


def send_leave_confirmation_to_student(student_name, receiver_email, text):
    """Send a confirmation email to a student"""
    email = "lenomadeleineantoine@gmail.com"
    subject = "Leave Request Approval"

    status_color = "green" if text.lower() == "approved" else "red"


    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Campusstay</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    color: #333;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    max-width: 600px;
                    margin: auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                }}
                .header {{
                    text-align: center;
                    background-color: #0044cc;
                    color: #ffffff;
                    padding: 20px;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    margin: 20px 0;
                    text-align: left;
                }}
                .content p {{
                    margin: 15px 0;
                    line-height: 1.6;
                }}
                .status {{
                    color: {status_color};
                    font-weight: bold;
                }}
                .footer {{
                    margin-top: 30px;
                    background-color: #f4f4f4;
                    text-align: center;
                    padding: 10px;
                    border-radius: 0 0 10px 10px;
                    font-size: 12px;
                    color: #888;
                }}
                .footer a {{
                    color: #0044cc;
                    text-decoration: none;
                }}
                .footer a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>Campusstay</h2>
                </div>
                <div class="content">
                    <p>Dear {student_name},</p>
                    <p>Your leave request has been successfully processed by the student affairs department and your school.</p>
                    <p>The status of your request is: <span class="status">{text}</span>.</p>
                    <p>Thank you for using Campusstay. If you have any questions or concerns, feel free to reach out to us.</p>
                </div>
                <div class="footer">
                    <p>&copy; {datetime.datetime.now().year} Campusstay. All Rights Reserved.</p>
                    <p>
                        For inquiries, contact us at 
                        <a href="mailto:support@campusstay.com">support@campusstay.com</a> 
                        or visit our website at 
                        <a href="https://www.campusstay.com">www.campusstay.com</a>.
                    </p>
                </div>
            </div>
        </body>
    </html>
    """



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
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")
