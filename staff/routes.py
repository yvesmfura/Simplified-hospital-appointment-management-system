from flask import render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import db, User, Client, Staff, Service, Feedback,Insurance, Appointment, Notification
from enum import Enum
from datetime import datetime
from . import staff_bp
from sqlalchemy.orm import joinedload

# Enum definitions
class UserRole(Enum):
    CLIENT = 'client'
    STAFF = 'staff'
    ADMIN = 'admin'

class GenderType(Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

# Login page
@staff_bp.route('/')
def staff_login():
    return render_template('staff/stafflogin.html')

# Logging in
@staff_bp.route('/login', methods=['GET', 'POST'])
def staff_auth():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            if user.role == UserRole.STAFF.value:
                session['user_id'] = user.user_id
                session['role'] = user.role
                
                staff_member = Staff.query.filter_by(user_id=user.user_id).first()
                session['full_name'] = staff_member.full_name if staff_member else 'Unknown'
                return redirect(url_for('staff.staff_dashboard'))
            else:
                flash('Access denied. Please log in through the correct portal.', 'error')
                return render_template('staff/stafflogin.html')
        else:
            flash('Invalid email or password. Please try again.', 'error')
            return render_template('staff/stafflogin.html')
    return render_template('staff/stafflogin.html')

# Accessing the STAFF portal dashboard
@staff_bp.route('/dashboard')
def staff_dashboard():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('staff.staff_login'))

    full_name = session.get('full_name', 'Staff Member')
    return render_template('staff/dashboard.html', full_name=full_name)

# Logging out of the system
@staff_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('staff.staff_login'))

# Fetching user profile from the database
@staff_bp.route('/profile')
def view_profile():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user:
            user_profile = {
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
            return render_template('staff/profile.html', user_profile=user_profile)
        else:
            flash('User not found.', 'error')
            return redirect(url_for('staff.staff_dashboard'))
    else:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('staff.staff_login'))

# Editing and updating user profile
@staff_bp.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user:
            if request.method == 'POST':
                email = request.form.get('email')
                username = request.form.get('username')
                password = request.form.get('password')
                password_confirm = request.form.get('password_confirm')

                user.email = email
                user.username = username

                if password and password == password_confirm:
                    user.password = generate_password_hash(password)
                elif password and password != password_confirm:
                    flash('Passwords do not match', 'error')
                    return redirect(url_for('staff.edit_profile'))

                try:
                    db.session.commit()
                    flash('Profile updated successfully', 'success')
                except Exception as e:
                    db.session.rollback()
                    flash(f'Error updating profile: {str(e)}', 'error')
                    
                return redirect(url_for('staff.view_profile'))
            return render_template('staff/edit_profile.html', user=user)
        else:
            flash('User not found.', 'error')
            return redirect(url_for('staff.staff_dashboard'))
    else:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('staff.staff_login'))

# Dynamic searching and fetching of client data
@staff_bp.route('/search/client', methods=['GET'])
def search_client():
    query = request.args.get('query', '')
    if query:
        clients = Client.query.filter(
            (Client.full_name.ilike(f'%{query}%')) | (Client.client_id.ilike(f'%{query}%'))
        ).all()
    else:
        clients = []

    client_list = [{
        'full_name': client.full_name,
        'client_id': client.client_id,
        'date_of_birth': client.date_of_birth.strftime('%Y-%m-%d'),
        'gender': client.gender,
        'contact_number': client.contact_number,
        'insurance': client.insurance
    } for client in clients]

    return jsonify(client_list)

# Managing appointments
@staff_bp.route('/appointments', methods=['GET'])
def get_appointments():
    if 'user_id' not in session or session.get('role') != 'staff':
        flash('Please log in as a staff member to access this page.', 'error')
        return redirect(url_for('staff.staff_login'))

    user_id = session['user_id']
    staff_member = Staff.query.filter_by(user_id=user_id).first()

    if not staff_member:
        flash('No staff member found for the given user.', 'error')
        return redirect(url_for('staff.staff_dashboard'))

    staff_id = staff_member.staff_id
    appointments = Appointment.query.options(joinedload(Appointment.client)).filter_by(staff_id=staff_id).all()

    appointment_list = []
    for appointment in appointments:
        client_info = {
            'full_name': appointment.client.full_name if appointment.client else 'N/A',
            'client_id': appointment.client.client_id if appointment.client else 'N/A',
            'date_of_birth': appointment.client.date_of_birth.strftime('%Y-%m-%d') if appointment.client else 'N/A',
            'gender': appointment.client.gender if appointment.client else 'N/A',
            'contact_number': appointment.client.contact_number if appointment.client else 'N/A',
            'insurance': appointment.client.insurance if appointment.client else 'N/A'
        }
        appointment_data = {
            'appointment_id': appointment.appointment_id,
            'client': client_info,
            'staff_id': appointment.staff_id,
            'appointment_date': appointment.appointment_date.strftime('%Y-%m-%d %H:%M:%S'),
            'service': appointment.service,
            'status': appointment.status
        }
        appointment_list.append(appointment_data)

    return render_template('staff/my_appointment.html', appointments=appointment_list)

@staff_bp.route('/reschedule', methods=['POST'])
def reschedule_appointment():
    if request.method == 'POST':
        appointment_id = request.json.get('appointmentId')
        new_date = request.json.get('newDate')
        client_id = request.json.get('clientId')

        if not appointment_id or not new_date or not client_id:
            return jsonify({'success': False, 'message': 'Missing data for rescheduling.'}), 400

        try:
            # Fetch the appointment
            appointment = Appointment.query.get(appointment_id)
            if not appointment:
                return jsonify({'success': False, 'message': 'Appointment not found.'}), 404

            # Update the appointment date
            appointment.appointment_date = datetime.strptime(new_date, '%Y-%m-%d %H:%M:%S')
            db.session.commit()

            # Fetch the client to get the user_id for notification
            client = Client.query.filter_by(client_id=client_id).first()
            if not client:
                return jsonify({'success': False, 'message': 'Client not found.'}), 404
            
            user_id = client.user_id

            # Create a notification
            notification_message = f'Your appointment has been rescheduled to {new_date}.'
            notification = Notification(
                sender_id=session['user_id'],
                recipient_id=user_id,
                message=notification_message,
                timestamp=datetime.now(),
                status='unread'
            )
            db.session.add(notification)
            db.session.commit()

            return jsonify({'success': True, 'message': 'Appointment rescheduled and notification sent successfully.'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Error rescheduling appointment: {str(e)}'}), 500


# Fetch patient details for viewing
@staff_bp.route('/patient-details/<client_id>', methods=['GET'])
def view_patient_details(client_id):
    client = Client.query.filter_by(client_id=client_id).first()
    if client:
        patient_details = {
            'full_name': client.full_name,
            'date_of_birth': client.date_of_birth.strftime('%Y-%m-%d'),
            'gender': client.gender,
            'contact_number': client.contact_number,
            'insurance': client.insurance,
            'marital_status': client.marital_status,
            'occupation': client.occupation,
            'next_of_kin': client.next_of_kin,
            'address_country': client.address_country,
            'address_district': client.address_district,
            'address_sector': client.address_sector,
            'address_village': client.address_village,
            'address_cell': client.address_cell
        }
        return jsonify(patient_details), 200
    else:
        return jsonify({'message': 'Patient not found.'}), 404

# Handling notifications
@staff_bp.route('/notifications', methods=['GET'])
def view_notifications():
    if 'user_id' not in session or session.get('role') != 'staff':
        flash('Please log in as a staff member to view notifications.', 'error')
        return redirect(url_for('staff.staff_login'))

    notifications = Notification.query.filter_by(recipient_id=session['user_id']).order_by(Notification.timestamp.desc()).all()

    return render_template('staff/notifications.html', notifications=notifications)

@staff_bp.route('/notify', methods=['POST'])
def notify_client():
    if 'user_id' not in session or session.get('role') != 'staff':
        flash('Please log in as a staff member to send notifications.', 'error')
        return redirect(url_for('staff.staff_login'))

    if request.method == 'POST':
        client_id = request.form.get('client_id')
        message = request.form.get('message')
        staff_username = session.get('full_name')
        current_date = datetime.now()

        if not client_id or not message:
            flash('Client ID and message are required.', 'error')
            return redirect(url_for('staff.staff_dashboard'))

        try:
            client = Client.query.filter_by(client_id=client_id).first()
            if not client:
                flash('Client not found.', 'error')
                return redirect(url_for('staff.staff_dashboard'))

            recipient_id = client.user_id
            notification = Notification(
                sender_id=session['user_id'],
                recipient_id=recipient_id,
                message=message,
                timestamp=current_date,
                status='unread'
            )

            db.session.add(notification)
            db.session.commit()

            flash('Notification sent successfully!', 'success')
            return redirect(url_for('staff.staff_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while sending the notification: {str(e)}', 'error')
            return redirect(url_for('staff.staff_dashboard'))

# Handling feedback submission
@staff_bp.route('/feedback', methods=['POST'])
def store_feedback():
    if request.method == 'POST':
        message = request.form.get('message')
        user_id = session.get('user_id')

        feedback = Feedback(
            user_id=user_id,
            message=message,
            feedback_date=datetime.now()
        )

        try:
            db.session.add(feedback)
            db.session.commit()
            flash('Feedback submitted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error submitting feedback: {str(e)}', 'error')

        return redirect(url_for('staff.staff_dashboard'))
