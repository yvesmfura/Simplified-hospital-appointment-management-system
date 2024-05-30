#!/bin/bash

# Create directories
mkdir -p app
mkdir -p models
mkdir -p templates/admin
mkdir -p templates/client
mkdir -p templates/staff
mkdir -p static/css
mkdir -p static/js
mkdir -p static/img

# Create files
touch app/app.py
touch models/models.py
touch templates/admin/admin_dashboard.html
touch templates/client/client_dashboard.html
touch templates/staff/staff_dashboard.html
touch templates/about.html
touch templates/adminlogin.html
touch templates/clientlogin.html
touch templates/forgotpassword.html
touch templates/index.html
touch templates/signup.html
touch static/css/style.css
touch static/js/script.js
touch static/img/your_image.png
touch config.py
touch requirements.txt
touch run.py

echo "File structure created successfully!"

