# Simplified Hospital Appointments Management System (SHAMS)

<img width="134" alt="OUR_SYSTEM_LOGO_SHAS" src="https://github.com/yvesmfura/Simplified-hospital-appointment-management-system/assets/132387277/58b3e479-3825-41ba-b7cd-53c5b54cf046">


## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Authors](#authors)
- [License](#license)

## Introduction

The Simplified Hospital Appointments Management System (SHAMS) is a comprehensive solution designed to streamline the appointment management process in hospitals. Developed to enhance healthcare access and efficiency, SHAMS provides a user-friendly platform for patients to book appointments, doctors to manage their schedules, and administrators to oversee the system.

## Features

- **Appointment Booking**: Patients can easily book appointments for specific medical services.
- **Doctor Schedule Management**: Doctors can efficiently manage their appointment schedules, update availability, and reschedule appointments as needed.
- **Administrative Controls**: Administrators have access to a comprehensive dashboard for managing user accounts, roles, system settings, and performance monitoring.

## Architecture

![SHAMS Architecture Diagram](link_to_architecture_diagram)

The SHAMS system architecture is designed to ensure seamless data flow and robust performance. The backend is powered by Flask, with SQLite as the database management system. Frontend development utilizes HTML5, CSS3, and JavaScript to deliver a responsive and intuitive user interface.

## Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Flask
- **Database**: SQLite
- **Notifications**: Email (system notifications)

## Installation

1. Clone the repository: `git clone https://github.com/your_username/shams.git`
2. Navigate to the project directory: `cd shams`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the development server: `python app.py`

## Usage

1. Access the SHAMS web application through the provided URL.
2. Register as a patient, doctor, or administrator, depending on your role. Only clients can sign up, while staff and admins will be added through the admin portal. Initial admin will be added manually into the database.
3. Explore the respective features based on your user role (e.g., booking appointments, managing schedules, overseeing system administration).
4. The system has an internal notification system to communicate between users.
5. Hospitals can integrate the system into their websites, allowing clients to visit the hospital website and request appointments. The system is centralized to enhance security and easy management across multiple hospitals.

## Contributing

We welcome contributions from the community! If you'd like to contribute to SHAMS, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request.

## Authors

- Yves Irakoze Mfura ([GitHub](https://github.com/yvesmfura), [LinkedIn](www.linkedin.com/in/
yves-irakoze-mfura-203053252
))
- Twayinganyiki Leonce ([GitHub](link_to_leonce_github), [LinkedIn](link_to_leonce_linkedin))

## License

This project is licensed under the [MIT License](link_to_license).
