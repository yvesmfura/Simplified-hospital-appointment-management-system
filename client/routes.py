from flask import render_template, request, redirect, url_for, flash, current_app, session, jsonify
from flask_mail import Message
from models.models import User, db, Notification, Client, Service, Appointment,Schedule, Feedback
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import client_bp
from enum import Enum


# Enum definitions
class UserRole(Enum):
    CLIENT = 'client'
    STAFF = 'staff'
    ADMIN = 'admin'

# Route for rendering the login page
@client_bp.route('/')
def client_login():
    return render_template('client/clientlogin.html')

# Logging in
@client_bp.route('/login', methods=['GET', 'POST'])
def client_auth():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                if user.role == UserRole.CLIENT.value:
                    session['user_id'] = user.user_id
                    session['role'] = user.role
                    return redirect(url_for('client.client_dashboard'))
                else:
                    flash('Access denied. Please log in through the correct portal.', 'error')
            else:
                flash('Invalid password. Please try again.', 'error')
        else:
            flash('Invalid email or password. Please try again.', 'error')
        
        return render_template('client/clientlogin.html')
    
    return render_template('client/clientlogin.html')

# Accessing the CLIENT portal dashboard
@client_bp.route('/dashboard')
def client_dashboard():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('client.client_login'))

    user = User.query.get(session['user_id'])
    full_name = user.username if user else None
    return render_template('client/dashboard.html', full_name=full_name)


# Route for user registration
@client_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if the email already exists in the database
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists.', 'error')
            return render_template('client/signup.html')
        
        # If the email does not exist, create a new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password, role='client')
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('client.client_login'))
    
    return render_template('client/signup.html')

# Route for user logout
@client_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()  # Clear the session upon logout
    flash('You have been logged out.', 'success')
    return redirect(url_for('client.client_login'))

# Route for handling forgot password functionality
@client_bp.route('/forgotpassword', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            send_password_email(user.email, user.password)  # Consider email security implications
            flash('An email containing your password has been sent to your email address.')
            return redirect(url_for('client.client_login'))  # Redirect to appropriate route
        else:
            flash('Email address not found.')
    return render_template('client/forgotpassword.html')

# Function to send password recovery email
def send_password_email(email, password):
    msg = Message('Password Recovery', sender=current_app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f'Your password is: {password}'
    mail = current_app.extensions.get('mail')
    mail.send(msg)

    
# Route for rendering the profile page
@client_bp.route('/profile')
def view_profile():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user:
            # Serialize the user profile data into JSON format
            user_profile = {
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'role': user.role  # Accessing Enum value
                # Add more fields as needed
            }
            return render_template('client/profile.html', user_profile=user_profile)
        else:
            flash('User not found.', 'error')
            return redirect(url_for('client.client_dashboard'))
    else:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('client.client_login'))

# Handling notifications
@client_bp.route('/notifications', methods=['GET'])
def view_notifications():
    if 'user_id' not in session or session.get('role') != 'client':
        flash('Please log in as a client to view notifications.', 'error')
        return redirect(url_for('client.client_login'))

    notifications = Notification.query.filter_by(recipient_id=session['user_id']).order_by(Notification.timestamp.desc()).all()

    return render_template('client/notifications.html', notifications=notifications)


# Route for rendering the request appointment page
@client_bp.route('/request_appointment')
def request_appointment_page():
    return render_template('client/request_appointment.html')


# Route for fetching services
@client_bp.route('/services', methods=['GET'])
def get_services():
    try:
        # Query the Service model to get all services
        services = Service.query.all()
        
        # Serialize the services into a list of dictionaries
        services_list = [{'service_id': service.service_id, 'name': service.name} for service in services]
        
        # Return the services as JSON
        return jsonify({'services': services_list}), 200
    except Exception as e:
        # Handle any errors that occur
        return jsonify({'error': str(e)}), 500
    
# Route for rendering the service page
@client_bp.route('/service')
def view_services():
    services = Service.query.all()
    return render_template('client/service.html', services=services)

@client_bp.route('/submit_appointment', methods=['POST'])
def submit_appointment():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Extracting patient details from the request data
        full_name = data.get('full_name')
        date_of_birth = data.get('date_of_birth')
        gender = data.get('gender')
        contact_number = data.get('contact_number')
        insurance = data.get('insurance')
        marital_status = data.get('marital_status')
        occupation = data.get('occupation')
        next_of_kin = data.get('next_of_kin')
        address_country = data.get('address_country')
        address_district = data.get('address_district')
        address_sector = data.get('address_sector')
        address_village = data.get('address_village')
        address_cell = data.get('address_cell')
        service_ID = data.get('service')
        appointment_date_time = data.get('appointment_date_time')

        # Debugging logs
        current_app.logger.debug(f'Received data: {data}')
        
        # Check for required fields
        if not all([full_name, date_of_birth, gender, service_ID, appointment_date_time]):
            current_app.logger.debug('Missing required fields')
            return jsonify({'message': 'Missing required fields'}), 400
        
        # Convert string dates to datetime objects
        try:
            date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d')
            appointment_date_time = datetime.strptime(appointment_date_time, '%Y-%m-%dT%H:%M')
        except ValueError as e:
            current_app.logger.debug('Invalid date format')
            return jsonify({'message': 'Invalid date format'}), 400
        
        # Fetch the service from the database
        service = Service.query.get(service_ID)
        if not service:
            current_app.logger.debug('Service not found')
            return jsonify({'message': 'Service not found'}), 404
        
        # Debug output for received service ID and service name
        current_app.logger.debug(f'Service found: {service.name} (ID: {service.service_id})')

        # Check if there is staff available for the given service
        staff_schedule = Schedule.query.filter_by(service_id=service_ID).first()
        current_app.logger.debug(f'Schedule query result for service ID {service_ID}: {staff_schedule}')

        if not staff_schedule:
            current_app.logger.debug(f'No staff available for service ID: {service_ID}')
            return jsonify({'message': 'No staff available for the selected service'}), 404
        
        # Assuming the user is already authenticated and their user_id is available in the session
        user_id = session.get('user_id')
        if not user_id:
            current_app.logger.debug('User not authenticated')
            return jsonify({'message': 'User not authenticated'}), 401
        
        # Verify user is a client
        user = User.query.get(user_id)
        if user.role != 'client':
            current_app.logger.debug('Only clients can book appointments')
            return jsonify({'message': 'Only clients can book appointments'}), 403
        
        # Debug output for user ID and role
        current_app.logger.debug(f'User: {user.username} (ID: {user.user_id}, Role: {user.role})')

        # Check if the client already exists for this user and the specified family member details
        client = Client.query.filter_by(
            user_id=user_id,
            full_name=full_name,
            date_of_birth=date_of_birth,
            gender=gender
        ).first()

        if client:
            current_app.logger.debug(f'Client found: {client.full_name} (ID: {client.client_id})')
        else:
            current_app.logger.debug(f'Client not found, creating new client: {full_name}')
            # Create a new client record only if it does not exist
            client = Client(
                user_id=user_id,
                full_name=full_name,
                date_of_birth=date_of_birth,
                gender=gender,
                contact_number=contact_number,
                insurance=insurance,
                marital_status=marital_status,
                occupation=occupation,
                next_of_kin=next_of_kin,
                address_country=address_country,
                address_district=address_district,
                address_sector=address_sector,
                address_village=address_village,
                address_cell=address_cell
            )
            db.session.add(client)
            db.session.commit()
            current_app.logger.debug(f'New client created with ID: {client.client_id}')

        # Check if the family member already has an appointment for the same service on the same day
        existing_appointment = Appointment.query.filter(
            Appointment.client_id == client.client_id,
            Appointment.service == service.name,
            db.func.date(Appointment.appointment_date) == appointment_date_time.date()
        ).first()

        if existing_appointment:
            current_app.logger.debug('This family member already has an appointment for this service on the same day')
            return jsonify({'message': 'This family member already has an appointment for this service on the same day'}), 400
        
        # Use the staff ID from the schedule for the appointment
        staff_id = staff_schedule.staff_id
        
        # Create a new appointment record
        new_appointment = Appointment(
            user_id=user_id,
            client_id=client.client_id,  # Use the existing client_id or the newly created one
            staff_id=staff_id,
            appointment_date=appointment_date_time,
            service=service.name,  # Assuming service is stored as its name
            status='scheduled'
        )
        
        db.session.add(new_appointment)
        db.session.commit()
        current_app.logger.debug('Appointment scheduled successfully!')

        return jsonify({'message': 'Appointment scheduled successfully!'}), 200
    
    except Exception as e:
        # Rollback in case of an error
        db.session.rollback()
        current_app.logger.error(f'Error scheduling appointment: {str(e)}')
        return jsonify({'message': str(e)}), 500

    
# Route for fetching appointments
@client_bp.route('/check_appointments', methods=['GET'])
def get_appointments():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('client.client_login'))

    user_id = session['user_id']
    
    # Fetch the user's appointments using the user_id
    appointments = Appointment.query.filter_by(user_id=user_id).all()
    
    return render_template('client/check_appointments.html', appointments=appointments)


# Handling feedback submission
@client_bp.route('/feedback', methods=['POST'])
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

        return redirect(url_for('client.client_dashboard'))
