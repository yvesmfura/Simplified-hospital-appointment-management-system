from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from datetime import datetime, timezone
from sqlalchemy import event
import random
import string

db = SQLAlchemy()

def generate_id(role):
    prefix = ''
    if role == 'client':
        prefix = 'C'
    elif role == 'admin':
        prefix = 'A'
    elif role == 'staff':
        prefix = 'S'
    else:
        prefix = 'U'  # Default for unknown roles
    
    random_id = ''.join(random.choices(string.digits, k=9))
    return prefix + random_id

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.String(10), primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    role = db.Column(Enum('client', 'staff', 'admin', name='user_roles'), nullable=False)
    client = db.relationship('Client', back_populates='user', uselist=False)
    staff = db.relationship('Staff', back_populates='user', uselist=False)
    followups = db.relationship('FollowUp', back_populates='user')
    feedbacks = db.relationship('Feedback', back_populates='user')
    appointments = db.relationship('Appointment', back_populates='user')

class Client(db.Model):
    __tablename__ = 'client'
    client_id = db.Column(db.String(10), primary_key=True)
    user_id = db.Column(db.String(10), db.ForeignKey('user.user_id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(Enum('male', 'female', 'other', name='gender_types'), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    insurance = db.Column(db.String(100), nullable=False)
    marital_status = db.Column(Enum('single', 'married', 'divorced', 'widowed', name='marital_status'), nullable=True)
    occupation = db.Column(db.String(100), nullable=True)
    next_of_kin = db.Column(db.String(100), nullable=True)
    address_country = db.Column(db.String(100), nullable=True)
    address_district = db.Column(db.String(100), nullable=True)
    address_sector = db.Column(db.String(100), nullable=True)
    address_village = db.Column(db.String(100), nullable=True)
    address_cell = db.Column(db.String(100), nullable=True)
    user = db.relationship('User', back_populates='client')
    appointments = db.relationship('Appointment', back_populates='client')

class Staff(db.Model):
    __tablename__ = 'staff'
    staff_id = db.Column(db.String(10), primary_key=True)
    user_id = db.Column(db.String(10), db.ForeignKey('user.user_id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    user = db.relationship('User', back_populates='staff')
    appointments = db.relationship('Appointment', back_populates='staff')
    schedules = db.relationship('Schedule', back_populates='staff')

class Appointment(db.Model):
    __tablename__ = 'appointment'
    appointment_id = db.Column(db.String(10), primary_key=True)
    user_id = db.Column(db.String(10), db.ForeignKey('user.user_id'), nullable=False)
    client_id = db.Column(db.String(10), db.ForeignKey('client.client_id'), nullable=False)
    staff_id = db.Column(db.String(10), db.ForeignKey('staff.staff_id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    service = db.Column(db.String(100), nullable=False)
    status = db.Column(Enum('scheduled', 'canceled', 'completed', name='appointment_status'), nullable=False)
    client = db.relationship('Client', back_populates='appointments')
    staff = db.relationship('Staff', back_populates='appointments')
    user = db.relationship('User', back_populates='appointments')

class FollowUp(db.Model):
    __tablename__ = 'followup'
    followup_id = db.Column(db.String(10), primary_key=True)
    user_id = db.Column(db.String(10), db.ForeignKey('user.user_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    followup_date = db.Column(db.DateTime, nullable=False)
    user = db.relationship('User', back_populates='followups')

class Insurance(db.Model):
    __tablename__ = 'insurance'
    insurance_id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Service(db.Model):
    __tablename__ = 'service'
    service_id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    head = db.Column(db.String(100), nullable=True)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    feedback_id = db.Column(db.String(10), primary_key=True)
    user_id = db.Column(db.String(10), db.ForeignKey('user.user_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    feedback_date = db.Column(db.DateTime, nullable=False)
    read = db.Column(db.Boolean, default=False)
    user = db.relationship('User', back_populates='feedbacks')

class Schedule(db.Model):
    __tablename__ = 'schedule'
    schedule_id = db.Column(db.String(13), primary_key=True)
    staff_id = db.Column(db.String(10), db.ForeignKey('staff.staff_id'), nullable=False)
    service_id = db.Column(db.String(10), db.ForeignKey('service.service_id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    staff = db.relationship('Staff', back_populates='schedules')
    service = db.relationship('Service', backref='schedules')

class Notification(db.Model):
    __tablename__ = 'notification'
    notification_id = db.Column(db.String(10), primary_key=True)
    sender_id = db.Column(db.String(10), db.ForeignKey('user.user_id'), nullable=False)
    recipient_id = db.Column(db.String(10), db.ForeignKey('user.user_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    status = db.Column(Enum('unread', 'read', name='notification_status'), nullable=False, default='unread')

    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_notifications')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_notifications')

# Event listener to generate IDs before inserting into the database
@event.listens_for(User, 'before_insert')
def generate_user_id(mapper, connection, target):
    target.user_id = generate_id(target.role)

@event.listens_for(Client, 'before_insert')
def generate_client_id(mapper, connection, target):
    target.client_id = generate_id('client')

@event.listens_for(Staff, 'before_insert')
def generate_staff_id(mapper, connection, target):
    target.staff_id = generate_id('staff')

@event.listens_for(Appointment, 'before_insert')
def generate_appointment_id(mapper, connection, target):
    target.appointment_id = 'AP' + ''.join(random.choices(string.digits, k=7))

@event.listens_for(FollowUp, 'before_insert')
def generate_followup_id(mapper, connection, target):
    target.followup_id = 'FU' + ''.join(random.choices(string.digits, k=7))

@event.listens_for(Insurance, 'before_insert')
def generate_insurance_id(mapper, connection, target):
    target.insurance_id = 'INS' + ''.join(random.choices(string.digits, k=7))

@event.listens_for(Service, 'before_insert')
def generate_service_id(mapper, connection, target):
    target.service_id = 'SVC' + ''.join(random.choices(string.digits, k=7))

@event.listens_for(Feedback, 'before_insert')
def generate_feedback_id(mapper, connection, target):
    target.feedback_id = 'FB' + ''.join(random.choices(string.digits, k=7))

@event.listens_for(Schedule, 'before_insert')
def generate_schedule_id(mapper, connection, target):
    target.schedule_id = 'SCH' + ''.join(random.choices(string.digits, k=7))

@event.listens_for(Notification, 'before_insert')
def generate_notification_id(mapper, connection, target):
    target.notification_id = 'NT' + ''.join(random.choices(string.digits, k=7))
