from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from models.models import db
from config import Config
from admin import admin_bp
from client import client_bp
from staff import staff_bp

app = Flask(__name__)
app.config.from_object(Config)
migrate = Migrate(app, db)
db.init_app(app)
mail = Mail(app)

# Register blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(client_bp)
app.register_blueprint(staff_bp)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signuppage')
def signuppage():
    return render_template('client/signup.html')

@app.route('/forgotpasswordpage')
def forgotpasspage():
    return render_template('client/forgotpassword.html')

if __name__ == '__main__':
    app.run(debug=True)
