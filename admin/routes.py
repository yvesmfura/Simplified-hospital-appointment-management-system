from flask import render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import db, User, Notification, Schedule, Feedback, Client, Staff, Appointment, FollowUp, Insurance, Service
from . import admin_bp
from enum import Enum
from datetime import datetime
from sqlalchemy import desc

@admin_bp.route('/')
def admin_login():
    return render_template('admin/adminlogin.html')

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_auth():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            if user.role == 'admin':
                session['user_id'] = user.user_id
                session['role'] = user.role
                return redirect(url_for('admin.admin_dashboard'))
            else:
                flash('Access denied. Please log in through the correct portal.', 'error')
                return render_template('admin/adminlogin.html')
        else:
            flash('Invalid email or password. Please try again.', 'error')
            return render_template('admin/adminlogin.html')
    return render_template('admin/adminlogin.html')

@admin_bp.route('/dashboard')
def admin_dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        return render_template('admin/dashboard.html', user=user)
    else:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('admin.admin_login'))

@admin_bp.route('/client/feedback_read/<int:feedback_id>', methods=['POST'])
def mark_feedback_as_read(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    feedback.read = True
    db.session.commit()
    return jsonify({'message': 'Feedback marked as read successfully'})

@admin_bp.route('/get_feedbacks')
def feedbacks():
    # Join Feedback and User tables to get the required data, sorted by date
    feedbacks = db.session.query(Feedback, User).join(User, Feedback.user_id == User.user_id).order_by(desc(Feedback.feedback_date)).all()
    
    # Create a list to hold the feedback details with user information
    feedback_list = []
    for feedback, user in feedbacks:
        feedback_list.append({
            'feedback_id': feedback.feedback_id,
            'user_id': feedback.user_id,
            'name': user.username,  # Assuming 'username' is the name field in User model
            'email': user.email,
            'date': feedback.feedback_date,
            'message': feedback.message,
            'read': feedback.read
        })
    
    # Render the template with the feedback data
    return render_template('admin/feedbacks.html', feedbacks=feedback_list)

@admin_bp.route('/profile')
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
            return render_template('admin/profile.html', user_profile=user_profile)
        else:
            flash('User not found.', 'error')
            return redirect(url_for('admin.admin_dashboard'))
    else:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('admin.admin_login'))

@admin_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('admin.admin_login'))

class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

@admin_bp.route('/profile/edit', methods=['GET', 'POST'])
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
                    return redirect(url_for('admin.edit_profile'))

                try:
                    db.session.commit()
                    flash('Profile updated successfully', 'success')
                except Exception as e:
                    db.session.rollback()
                    flash('Error updating profile: {}'.format(e), 'error')
                    
                return redirect(url_for('admin.view_profile'))
            return render_template('admin/edit_profile.html', user=user)
        else:
            flash('User not found.', 'error')
            return redirect(url_for('admin.admin_dashboard'))
    else:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('admin.admin_login'))


@admin_bp.route('/notify', methods=['POST'])
def notify_client():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Please log in as an admin to send notifications.', 'error')
        return redirect(url_for('admin.admin_login'))

    recipient_id = request.form.get('user_id')
    message = request.form.get('message')
    current_date = datetime.now()
    print(recipient_id)

    try:
        recipient = User.query.filter_by(user_id=recipient_id).first()
        if not recipient:
            flash('Recipient not found.', 'error')
            return redirect(url_for('admin.feedbacks'))

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
        return redirect(url_for('admin.feedbacks'))
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred while sending the notification: {str(e)}', 'error')
        return redirect(url_for('admin.admin_dashboard'))
    
# Dynamic searching and fetching of user data
@admin_bp.route('/search/user', methods=['GET'])
def search_user():
    query = request.args.get('query', '')
    if query:
        users = User.query.filter(
            (User.username.ilike(f'%{query}%')) | (User.user_id.ilike(f'%{query}%')) | (User.email.ilike(f'%{query}%'))
        ).all()
    else:
        users = []

    user_list = [{
        'user_id': user.user_id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    } for user in users]

    return jsonify(user_list)

# Dynamic searching and fetching of client data
@admin_bp.route('/search/client', methods=['GET'])
def search_client():
    query = request.args.get('query', '')
    if query:
        clients = Client.query.filter(
            (Client.full_name.ilike(f'%{query}%')) | (Client.client_id.ilike(f'%{query}%')) | (Client.contact_number.ilike(f'%{query}%'))
        ).all()
    else:
        clients = []

    client_list = [{
        'user_id': client.user_id,
        'client_id': client.client_id,
        'full_name': client.full_name,
        'date_of_birth': client.date_of_birth.isoformat(),
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
    } for client in clients]

    return jsonify(client_list)

# Dynamic searching and fetching of staff data
@admin_bp.route('/search/staff', methods=['GET'])
def search_staff():
    query = request.args.get('query', '')
    if query:
        staff_members = Staff.query.filter(
            (Staff.full_name.ilike(f'%{query}%')) | (Staff.staff_id.ilike(f'%{query}%')) | (Staff.specialization.ilike(f'%{query}%'))
        ).all()
    else:
        staff_members = []

    staff_list = [{
        'staff_id': staff.staff_id,
        'user_id': staff.user_id,
        'full_name': staff.full_name,
        'specialization': staff.specialization,
        'contact_number': staff.contact_number
    } for staff in staff_members]

    return jsonify(staff_list)

# Dynamic searching and fetching of appointment data
@admin_bp.route('/search/appointment', methods=['GET'])
def search_appointment():
    query = request.args.get('query', '')
    if query:
        appointments = Appointment.query.filter(
            (Appointment.user_id.ilike(f'%{query}%')) | 
            (Appointment.client_id.ilike(f'%{query}%')) |
            (Appointment.staff_id.ilike(f'%{query}%')) |
            (Appointment.service.ilike(f'%{query}%')) |
            (Appointment.status.ilike(f'%{query}%'))
        ).all()
    else:
        appointments = []

    appointment_list = [{
        'appointment_id': appointment.appointment_id,
        'user_id': appointment.user_id,
        'client_id': appointment.client_id,
        'client_full_name': Client.query.get(appointment.client_id).full_name,
        'staff_id': appointment.staff_id,
        'appointment_date': appointment.appointment_date.isoformat(),
        'service': appointment.service,
        'status': appointment.status
    } for appointment in appointments]
    return jsonify(appointment_list)


# Dynamic searching and fetching of notification data
@admin_bp.route('/search/notification', methods=['GET'])
def search_notification():
    query = request.args.get('query', '')
    if query:
        notifications = Notification.query.filter(
            (Notification.sender_id.ilike(f'%{query}%')) |
            (Notification.recipient_id.ilike(f'%{query}%'))
        ).all()
    else:
        notifications = []

    notification_list = [{
        'notification_id': notification.notification_id,
        'sender_id': notification.sender_id,
        'recipient_id': notification.recipient_id,
        'message': notification.message,
        'timestamp': notification.timestamp.isoformat(),
        'status': notification.status
    } for notification in notifications]

    return jsonify(notification_list)

# Dynamic searching and fetching of feedback data by user id
@admin_bp.route('/search/feedback', methods=['GET'])
def search_feedback():
    query = request.args.get('query', '')
    if query:
        feedbacks = Feedback.query.filter(
            (Feedback.message.ilike(f'%{query}%')) |
            (Feedback.user_id.ilike(f'%{query}%'))
        ).all()
    else:
        feedbacks = []

    feedback_list = [{
        'feedback_id': feedback.feedback_id,
        'user_id': feedback.user_id,
        'message': feedback.message,
        'feedback_date': feedback.feedback_date.isoformat(),
        'read': feedback.read
    } for feedback in feedbacks]

    return jsonify(feedback_list)



@admin_bp.route('/edit_user', methods=['POST'])
def edit_user():
    data = request.json
    user_id = data.get('user_id')
    username = data.get('username')
    role = data.get('role')
    email = data.get('email')

    # Implement your logic to handle updating the user details
    # For example, update the user in the database
    try:
        user = User.query.get(user_id)
        if user:
            user.username = username
            user.role = role
            user.email = email
            db.session.commit()
            return jsonify({'success': True, 'message': 'User details updated successfully!'})
        else:
            return jsonify({'success': False, 'message': 'User not found!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    
@admin_bp.route('/create/staff', methods=['POST'])
def create_new_staff():
    # Retrieve data from the request
    data = request.json
    full_name = data.get('full_name')
    username = data.get('username')
    email = data.get('email')
    contact_number = data.get('contact_number')
    specialization = data.get('specialization')
    role = data.get('role')
    password = data.get('password')

    if not (full_name and username and email and contact_number and specialization and role and password):
        return jsonify({'success': False, 'message': 'All fields are required'}), 400

    try:
        # Check if the username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return jsonify({'success': False, 'message': 'Username or email already exists'}), 400

        # Create a new User
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            role=role
        )
        db.session.add(new_user)
        db.session.flush()  # Flush to get the new user's id

        # Create a new Staff entry linked to the new User
        new_staff = Staff(
            user_id=new_user.user_id,  # Link to the User's ID
            full_name=full_name,
            contact_number=contact_number,
            specialization=specialization
        )
        db.session.add(new_staff)
        db.session.commit()  # Commit both User and Staff to the database

        return jsonify({'success': True, 'message': 'Staff created successfully', 'staff_id': new_staff.staff_id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error creating staff: {str(e)}'}), 500
    
@admin_bp.route('/get/staff/<staff_id>', methods=['GET'])
def get_staff(staff_id):
    staff = Staff.query.get(staff_id)
    if staff:
        staff_data = {
            'staff_id': staff.staff_id,
            'full_name': staff.full_name,
            'specialization': staff.specialization,
            'contact_number': staff.contact_number,
        }
        return jsonify(staff_data)
    return jsonify({'error': 'Staff not found'}), 404

@admin_bp.route('/edit/staff/<staff_id>', methods=['POST'])
def edit_staff(staff_id):
    data = request.json
    staff = Staff.query.get(staff_id)
    if staff:
        staff.full_name = data.get('full_name', staff.full_name)
        staff.specialization = data.get('specialization', staff.specialization)
        staff.contact_number = data.get('contact_number', staff.contact_number)
        try:
            db.session.commit()
            flash('Staff updated successfully!', 'success')
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 500
    return jsonify({'success': False, 'message': 'Staff not found'}), 404


# Dynamic searching and fetching of service data
@admin_bp.route('/search/service', methods=['GET'])
def search_service():
    query = request.args.get('query', '')
    if query:
        services = Service.query.filter(
            (Service.name.ilike(f'%{query}%')) | (Service.service_id.ilike(f'%{query}%')) | (Service.head.ilike(f'%{query}%'))
        ).all()
    else:
        services = []

    service_list = [{
        'service_id': service.service_id,
        'name': service.name,
        'head': service.head
    } for service in services]

    return jsonify(service_list)


@admin_bp.route('/get/service/<service_id>', methods=['GET'])
def get_service(service_id):
    service = Service.query.get(service_id)
    if service:
        service_data = {
            'service_id': service.service_id,
            'name': service.name,
            'head': service.head,
        }
        return jsonify(service_data)
    return jsonify({'error': 'Service not found'}), 404

@admin_bp.route('/edit/service/<service_id>', methods=['POST'])
def edit_service(service_id):
    data = request.json
    service = Service.query.get(service_id)
    if service:
        service.name = data.get('name', service.name)
        service.head = data.get('head', service.head)
        try:
            db.session.commit()
            flash('Service updated successfully!', 'success')
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 500
    return jsonify({'success': False, 'message': 'Service not found'}), 404


@admin_bp.route('/search/insurance', methods=['GET'])
def search_insurance():
    query = request.args.get('query', '')
    if query:
        insurances = Insurance.query.filter(
            (Insurance.name.ilike(f'%{query}%')) | (Insurance.insurance_id.ilike(f'%{query}%'))
        ).all()
    else:
        insurances = []

    insurance_list = [{
        'insurance_id': insurance.insurance_id,
        'name': insurance.name,
    } for insurance in insurances]

    return jsonify(insurance_list)

@admin_bp.route('/get/insurance/<insurance_id>', methods=['GET'])
def get_insurance(insurance_id):
    insurance = Insurance.query.get(insurance_id)
    if insurance:
        insurance_data = {
            'insurance_id': insurance.insurance_id,
            'name': insurance.name,
        }
        return jsonify(insurance_data)
    return jsonify({'error': 'Insurance not found'}), 404

@admin_bp.route('/edit/insurance/<insurance_id>', methods=['POST'])
def edit_insurance(insurance_id):
    data = request.json
    insurance = Insurance.query.get(insurance_id)
    if insurance:
        insurance.name = data.get('name', insurance.name)
        try:
            db.session.commit()
            flash('Insurance updated successfully!', 'success')
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 500
    return jsonify({'success': False, 'message': 'Insurance not found'}), 404

@admin_bp.route('/add/insurance', methods=['POST'])
def add_insurance():
    data = request.json
    new_insurance = Insurance(
        name=data['name']
    )
    try:
        db.session.add(new_insurance)
        db.session.commit()
        flash('Insurance added successfully!', 'success')
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    

# Dynamic searching and fetching of schedule data
@admin_bp.route('/search/schedule', methods=['GET'])
def search_schedule():
    query = request.args.get('query', '')
    if query:
        schedules = Schedule.query.filter(
            (Schedule.appointment_date.ilike(f'%{query}%')) |
            (Schedule.staff_id.ilike(f'%{query}%')) |
            (Schedule.service_id.ilike(f'%{query}%'))
        ).all()
    else:
        schedules = []

    schedule_list = [{
        'schedule_id': schedule.schedule_id,
        'staff_id': schedule.staff_id,
        'staff_name': Staff.query.get(schedule.staff_id).full_name,
        'service_id': schedule.service_id,
        'service_name': Service.query.get(schedule.service_id).name,
        'appointment_date': schedule.appointment_date.isoformat()
    } for schedule in schedules]

    return jsonify(schedule_list)


# Route to fetch staff names for dropdown
@admin_bp.route('/get/staff-names', methods=['GET'])
def get_staff_names():
    staff_list = Staff.query.all()
    staff_names = [{'staff_id': s.staff_id, 'staff_name': s.full_name} for s in staff_list]
    return jsonify(staff_names)

# Route to fetch service names for dropdown
@admin_bp.route('/get/service-names', methods=['GET'])
def get_service_names():
    service_list = Service.query.all()
    service_names = [{'service_id': s.service_id, 'service_name': s.name} for s in service_list]  # Use correct attribute name
    return jsonify(service_names)

# Route to update the schedule details
@admin_bp.route('/update/schedule', methods=['POST'])
def update_schedule():
    data = request.get_json()
    schedule_id = data.get('schedule_id')
    staff_id = data.get('staff_id')
    service_id = data.get('service_id')
    appointment_date = data.get('appointment_date')

    schedule = Schedule.query.get(schedule_id)
    if not schedule:
        return jsonify({'success': False, 'message': 'Schedule not found'}), 404

    try:
        schedule.staff_id = staff_id
        schedule.service_id = service_id
        schedule.start_time = datetime.strptime(appointment_date, '%Y-%m-%d %H:%M:%S')  # Update this if format is different
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Schedule updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500