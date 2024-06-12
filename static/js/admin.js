
document.getElementById('search-user').addEventListener('input', function() {
    const query = this.value;
    fetch(`/admin/search/user?query=${query}`)
    .then(response => response.json())
    .then(data => {
        const tableBody = document.getElementById('user-table-body');
        tableBody.innerHTML = '';
        data.forEach(user => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${user.username}</td>
            <td>${user.user_id}</td>
            <td>${user.role}</td>
            <td>${user.email}</td>
            <td>
            <button type="button" class="btn btn-primary edit-button" data-bs-toggle="modal" data-bs-target="#editUserModal" data-user-id="${user.user_id}" data-username="${user.username}" data-role="${user.role}" data-email="${user.email}">Edit</button>
            <button type="button" class="btn btn-primary notify-button" data-bs-toggle="modal" data-bs-target="#notifyModal" data-user-id="${user.user_id}">Notify</button>
            </td>
        `;
        tableBody.appendChild(row);
        });
        addEditButtonEventListeners();
        addNotifyButtonEventListeners();
    })
    .catch(error => console.error('Error fetching users:', error));
});


function addEditButtonEventListeners() {
    document.querySelectorAll('.edit-button').forEach(button => {
    button.addEventListener('click', function() {
        const userId = this.getAttribute('data-user-id');
        const username = this.getAttribute('data-username');
        const role = this.getAttribute('data-role');
        const email = this.getAttribute('data-email');

        document.getElementById('user-id').value = userId;
        document.getElementById('user-name').value = username;
        document.getElementById('user-role').value = role;
        document.getElementById('user-email').value = email;
    });
    });
}

function addNotifyButtonEventListeners() {
    document.querySelectorAll('.notify-button').forEach(button => {
        button.addEventListener('click', function() {
            const userId = this.getAttribute('data-user-id');
            document.getElementById('notifyUserId').value = userId;
        });
    });
}

document.getElementById('save-changes-btn').addEventListener('click', function() {
    const userId = document.getElementById('user-id').value;
    const username = document.getElementById('user-name').value;
    const role = document.getElementById('user-role').value;
    const email = document.getElementById('user-email').value;

    const userData = {
    user_id: userId,
    username: username,
    role: role,
    email: email
    };

    fetch('/admin/edit_user', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(userData)
    })
    .then(response => response.json())
    .then(data => {
    if (data.success) {
        alert('User details updated successfully!');
        // Optionally, you can refresh the user list or update the table directly
        document.getElementById('edit-user-form').reset();
        $('#editUserModal').modal('hide');
        // Optionally, re-fetch user data to update the table
        document.getElementById('search-user').dispatchEvent(new Event('input'));
    } else {
        alert('Failed to update user details: ' + data.message);
    }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('search-staff').addEventListener('input', function() {
    const query = this.value;
    fetch(`/admin/search/staff?query=${query}`)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('staff-table-body');
            tableBody.innerHTML = '';
            data.forEach(staff => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${staff.full_name}</td>
                    <td>${staff.user_id}</td>
                    <td>${staff.staff_id}</td>
                    <td>${staff.specialization}</td>
                    <td>
                        <button class="action-btn edit-staff" data-bs-toggle="modal" data-bs-target="#editStaffModal" data-staff-id="${staff.staff_id}">Edit Staff</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });

            document.querySelectorAll('.edit-staff').forEach(button => {
                button.addEventListener('click', function() {
                    const staffId = this.getAttribute('data-staff-id');
                    fetch(`/admin/get/staff/${staffId}`)
                        .then(response => response.json())
                        .then(staff => {
                            document.getElementById('staff-id').value = staff.staff_id;
                            document.getElementById('staff-name').value = staff.full_name;
                            document.getElementById('staff-specialization').value = staff.specialization;
                            document.getElementById('staff-contact').value = staff.contact_number;
                            document.getElementById('update-staff-button').setAttribute('data-staff-id', staffId);
                        })
                        .catch(error => console.error('Error fetching staff details:', error));
                });
            });
        })
        .catch(error => console.error('Error fetching staff:', error));
});

document.getElementById('update-staff-button').addEventListener('click', function() {
    const staffId = this.getAttribute('data-staff-id');
    const updatedStaff = {
        full_name: document.getElementById('staff-name').value,
        specialization: document.getElementById('staff-specialization').value,
        contact_number: document.getElementById('staff-contact').value,
    };

    fetch(`/admin/edit/staff/${staffId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedStaff),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Optionally update the UI or show a success message
            alert('Staff updated successfully!');
            location.reload();
        } else {
            alert('Failed to update staff');
        }
    })
    .catch(error => console.error('Error updating staff:', error));
});

document.getElementById('search-insurance').addEventListener('input', function() {
    const query = this.value;
    fetch(`/admin/search/insurance?query=${query}`)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('insurance-table-body');
            tableBody.innerHTML = '';
            data.forEach(insurance => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${insurance.name}</td>
                    <td>${insurance.insurance_id}</td>
                    <td>
                        <button type="button" class="btn btn-primary edit-insurance-button" data-bs-toggle="modal" data-bs-target="#editInsuranceModal" data-insurance-id="${insurance.insurance_id}" data-insurance-name="${insurance.name}">Edit Insurance</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
            addEditInsuranceButtonEventListeners();
        })
        .catch(error => console.error('Error fetching insurances:', error));
});

function addEditInsuranceButtonEventListeners() {
    document.querySelectorAll('.edit-insurance-button').forEach(button => {
        button.addEventListener('click', function() {
            const insuranceId = this.getAttribute('data-insurance-id');
            const insuranceName = this.getAttribute('data-insurance-name');

            document.getElementById('insurance-id').value = insuranceId;
            document.getElementById('insurance-name').value = insuranceName;
        });
    });
}

document.getElementById('search-schedule').addEventListener('input', function() {
    const query = this.value;
    fetch(`/admin/search/schedule?query=${query}`)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('schedule-table-body');
            tableBody.innerHTML = '';
            data.forEach(schedule => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${schedule.schedule_id}</td>
                    <td>${schedule.staff_id}</td>
                    <td>${schedule.staff_name}</td>
                    <td>${schedule.service_id}</td>
                    <td>${schedule.service_name}</td>
                    <td>${schedule.appointment_date}</td>
                    <td>
                        <button type="button" class="btn btn-primary edit-schedule-button" data-bs-toggle="modal" data-bs-target="#editScheduleModal" data-schedule-id="${schedule.schedule_id}" data-staff-id="${schedule.staff_id}" data-service-id="${schedule.service_id}" data-service-name="${schedule.service_name}" data-appointment-date="${schedule.appointment_date}">Edit Schedule</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
            addEditScheduleButtonEventListeners();
        })
        .catch(error => console.error('Error fetching schedules:', error));
});

function addEditScheduleButtonEventListeners() {
    document.querySelectorAll('.edit-schedule-button').forEach(button => {
        button.addEventListener('click', function() {
            const scheduleId = this.getAttribute('data-schedule-id');
            const staffId = this.getAttribute('data-staff-id');
            const serviceId = this.getAttribute('data-service-id');
            const serviceName = this.getAttribute('data-service-name');
            const appointmentDate = this.getAttribute('data-appointment-date');

            document.getElementById('schedule-id').value = scheduleId;
            document.getElementById('staff-id').value = staffId;
            document.getElementById('service-id').value = serviceId;
            document.getElementById('service-name').value = serviceName;
            document.getElementById('appointment-date').value = appointmentDate;
        });
    });
}

document.getElementById('search-notification').addEventListener('input', function() {
    const query = this.value;
    fetch(`/admin/search/notification?query=${query}`)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('notification-table-body');
            tableBody.innerHTML = '';
            data.forEach(notification => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${notification.notification_id}</td>
                    <td>${notification.sender_id}</td>
                    <td>${notification.recipient_id}</td>
                    <td>${notification.message}</td>
                    <td>${notification.timestamp}</td>
                    <td>${notification.status}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching notifications:', error));
});

document.getElementById('search-feedback').addEventListener('input', function() {
    const query = this.value;
    fetch(`/admin/search/feedback?query=${query}`)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('feedback-table-body');
            tableBody.innerHTML = '';
            data.forEach(feedback => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${feedback.feedback_id}</td>
                    <td>${feedback.user_id}</td>
                    <td>${feedback.message}</td>
                    <td>${feedback.feedback_date}</td>
                    <td>${feedback.read}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching feedbacks:', error));
});

document.getElementById('search-appointment').addEventListener('input', function() {
    const query = this.value;
    fetch(`/admin/search/appointment?query=${query}`)
    .then(response => response.json())
    .then(data => {
        const tableBody = document.getElementById('appointment-table-body');
        tableBody.innerHTML = '';
        data.forEach(appointment => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${appointment.appointment_id}</td>
            <td>${appointment.user_id}</td>
            <td>${appointment.client_id}</td>
            <td>${appointment.client_full_name}</td>
            <td>${appointment.staff_id}</td>
            <td>${appointment.service}</td>
            <td>${appointment.appointment_date}</td>
            <td>${appointment.status}</td>
        `;
        tableBody.appendChild(row);
        });
    })
    .catch(error => console.error('Error fetching appointments:', error));
});


document.getElementById('search-client').addEventListener('input', function() {
    const query = this.value;
    fetch(`/admin/search/client?query=${query}`)
    .then(response => response.json())
    .then(data => {
        const tableBody = document.getElementById('client-table-body');
        tableBody.innerHTML = '';
        data.forEach(client => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${client.full_name}</td>
            <td>${client.user_id}</td>
            <td>${client.client_id}</td>
            <td>${client.contact_number}</td>
            <td>${client.date_of_birth}</td>
        `;
        tableBody.appendChild(row);
        });
    })
    .catch(error => console.error('Error fetching clients:', error));
});

document.getElementById('createStaffBtn').addEventListener('click', function() {
    // Collect the form data
    const fullName = document.getElementById('new-staff-fullname').value;
    const username = document.getElementById('new-staff-username').value;
    const email = document.getElementById('new-staff-email').value;
    const contactNumber = document.getElementById('new-staff-contact-number').value;
    const specialization = document.getElementById('new-staff-specialization').value;
    const role = document.getElementById('new-staff-role').value;
    const password = document.getElementById('new-staff-password').value;
    const confirmPassword = document.getElementById('new-staff-confirm-password').value;

    // Check if password and confirm password match
    if (password !== confirmPassword) {
        alert('Passwords do not match!');
        return;
    }

    // Create the data object to send
    const staffData = {
        full_name: fullName,
        username: username,
        email: email,
        contact_number: contactNumber,
        specialization: specialization,
        role: role,
        password: password
    };

    // Send the data to the backend
    fetch('/admin/create/staff', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(staffData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Staff created successfully!');
            // Optionally close the modal
            const createStaffModal = new bootstrap.Modal(document.getElementById('createNewStaffModal'));
            createStaffModal.hide();

            // Optionally refresh the staff list or perform other UI updates
            // For example, you could trigger a fetch to update the staff table
            fetchStaffList();
        } else {
            alert('Error creating staff: ' + data.message);
        }
    })
    .catch(error => console.error('Error creating staff:', error));
});

// Example function to refresh the staff list
function fetchStaffList() {
    fetch('/admin/get/staff-list')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('staff-table-body');
            tableBody.innerHTML = '';
            data.forEach(staff => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${staff.full_name}</td>
                    <td>${staff.user_id}</td>
                    <td>${staff.staff_id}</td>
                    <td>${staff.specialization}</td>
                    <td>
                        <button class="action-btn edit-staff" data-bs-toggle="modal" data-bs-target="#editStaffModal">Edit Staff</button>
                        <button class="action-btn schedule-staff" data-bs-toggle="modal" data-bs-target="#scheduleStaffModal">Schedule Staff</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching staff:', error));
}

document.getElementById('createUserBtn').addEventListener('click', function() {
    // Collect the form data
    const username = document.getElementById('new-user-username').value;
    const password = document.getElementById('new-user-password').value;
    const role = document.getElementById('new-user-role').value;

    // Password confirmation
    const confirmPassword = document.getElementById('new-user-confirm-password').value;

    // Check if password and confirm password match
    if (password !== confirmPassword) {
        alert('Passwords do not match!');
        return;
    }

    // Create the data object to send
    const userData = {
        username: username,
        password: password,
        role: role
    };

    // Send the data to the backend
    fetch('/admin/create/user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('User created successfully!');
            // Optionally close the modal or perform other actions
            const createUserModal = new bootstrap.Modal(document.getElementById('createNewUserModal'));
            createUserModal.hide();
        } else {
            alert('Error creating user: ' + data.message);
        }
    })
    .catch(error => console.error('Error creating user:', error));
});


document.getElementById('search-service').addEventListener('input', function() {
    const query = this.value;
    fetch(`/admin/search/service?query=${query}`)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('service-table-body');
            tableBody.innerHTML = '';
            data.forEach(service => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${service.name}</td>
                    <td>${service.service_id}</td>
                    <td>${service.head}</td>
                    <td>
                        <button class="action-btn edit-service" data-bs-toggle="modal" data-bs-target="#editServiceModal" data-service-id="${service.service_id}">Edit Service</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });

            document.querySelectorAll('.edit-service').forEach(button => {
                button.addEventListener('click', function() {
                    const serviceId = this.getAttribute('data-service-id');
                    fetch(`/admin/get/service/${serviceId}`)
                        .then(response => response.json())
                        .then(service => {
                            document.getElementById('service-name').value = service.name;
                            document.getElementById('service-head').value = service.head;
                            document.getElementById('update-service-button').setAttribute('data-service-id', serviceId);
                        })
                        .catch(error => console.error('Error fetching service details:', error));
                });
            });
        })
        .catch(error => console.error('Error fetching services:', error));
});