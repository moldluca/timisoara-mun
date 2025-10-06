#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os

# Pentru debugging CGI pe server (decomentează dacă ai probleme)
# import cgitb
# cgitb.enable()

# Adaugă calea către aplicația ta (înlocuiește 'username' cu username-ul tău real de la Hostico)
# sys.path.insert(0, '/home/username/public_html/')

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv
from models import db, Registration
from functools import wraps
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

users = {
    "dragos@timisoara-mun.ro": "dragosSecretariatMunIntern",
    "cristiana@timisoara-mun.ro": "cristianaSecretariatMunIntern",
    "erol@timisoara-mun.ro": "erolSecretariatMunIntern",
    "secretariat@timisoara-mun.ro": "secretariatSecretariatMunIntern",
    "luca.vasiu@timisoara-mun.ro": "lucaSecretariatMunIntern",
    "delegate.registration@timisoara-mun.ro": "delegateSecretariatMunIntern",
    "luca.stefan@timisoara-mun.ro": "lucaSecretariatMunIntern"
}

app = Flask(__name__)

# Încarcă variabilele de mediu (pentru producție, folosește variabile de sistem)
try:
    load_dotenv()
except:
    pass

# Configurare Flask pentru producție
app.secret_key = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'False') == 'True'
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

# Configurare baza de date pentru producție
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///instance/tm_mun.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mail = Mail(app)
db.init_app(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

committees = {
    'unsc': {'name': 'United Nations Security Council', 'abbreviation': 'UNSC'},
    'unhrc': {'name': 'United Nations Human Rights Council', 'abbreviation': 'UNHRC'},
    'ecofin': {'name': 'Economic and Financial Committee', 'abbreviation': 'ECOFIN'},
    'sochum': {'name': 'Social, Humanitarian & Cultural Committee', 'abbreviation': 'SOCHUM'},
    'crisis': {'name': 'Crisis Committee', 'abbreviation': 'CRISIS'},
    'c24': {'name': 'Committee of 24', 'abbreviation': 'C-24'},
    'unodc': {'name': 'United Nations Office on Drugs and Crime', 'abbreviation': 'UNODC'},
    'ohchr': {'name': 'Office of the High Commissioner for Human Rights', 'abbreviation': 'OHCHR'},
    'who': {'name': 'World Health Organization', 'abbreviation': 'WHO'},
    'icj': {'name': 'International Court of Justice', 'abbreviation': 'ICJ'},
    'unicef': {'name': 'United Nations Children\'s Fund', 'abbreviation': 'UNICEF'},
    'disec': {'name': 'Disarmament and International Security Committee', 'abbreviation': 'DISEC'}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/whowe')
def whowe():
    return render_template('whowe.html')

@app.route('/advisors')
def advisors():
    return render_template('advisors.html')

@app.route('/chairmen')
def chairmen():
    return render_template('chairmen.html')

@app.route('/staff')
def staff():
    return render_template('staff.html')

@app.route('/totichair')
def totichair():
    return render_template('totichair.html')

@app.route('/org')
def org():
    return render_template('org.html')

@app.route('/parteneri')
def parteneri():
    return render_template('parteneri.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/comitete')
def comitete():
    return render_template('comitete.html')

@app.route('/committee/<committee_id>')
def committee(committee_id):
    committee_info = committees.get(committee_id)
    if not committee_info:
        return render_template('error.html'), 404
    return render_template('zaltapagina.html', committee=committee_info)

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/policies')
def policies():
    return render_template('policies.html')

@app.route('/privacy-terms')
def privacy_terms():
    return render_template('privacy-terms.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/delegates-registration', methods=['GET', 'POST'])
def delegates_registration():
    if request.method == 'POST':
        try:
            # Colectează datele din formular
            registration_data = {
                'first_name': request.form.get('first_name'),
                'last_name': request.form.get('last_name'),
                'email': request.form.get('email'),
                'phone': request.form.get('phone'),
                'school': request.form.get('school'),
                'grade': request.form.get('grade'),
                'committee_preference_1': request.form.get('committee_preference_1'),
                'committee_preference_2': request.form.get('committee_preference_2'),
                'committee_preference_3': request.form.get('committee_preference_3'),
                'country_preference_1': request.form.get('country_preference_1'),
                'country_preference_2': request.form.get('country_preference_2'),
                'country_preference_3': request.form.get('country_preference_3'),
                'experience': request.form.get('experience'),
                'dietary_requirements': request.form.get('dietary_requirements'),
                'emergency_contact': request.form.get('emergency_contact'),
                'emergency_phone': request.form.get('emergency_phone')
            }
            
            # Creează înregistrarea în baza de date
            registration = Registration(**registration_data)
            db.session.add(registration)
            db.session.commit()
            
            # Trimite email
            send_registration_email(registration_data)
            
            flash('Registration submitted successfully! You will receive a confirmation email shortly.', 'success')
            return redirect(url_for('delegates_registration'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'error')
    
    return render_template('delegates-registration.html')

def send_registration_email(registration_data):
    try:
        msg = Message(
            'New Delegate Registration - TimișoaraMUN 2025',
            sender=app.config['MAIL_USERNAME'],
            recipients=['delegate.registration@timisoara-mun.ro']
        )
        
        msg.body = f"""
New delegate registration received:

Name: {registration_data['first_name']} {registration_data['last_name']}
Email: {registration_data['email']}
Phone: {registration_data['phone']}
School: {registration_data['school']}
Grade: {registration_data['grade']}

Committee Preferences:
1. {registration_data['committee_preference_1']}
2. {registration_data['committee_preference_2']}
3. {registration_data['committee_preference_3']}

Country Preferences:
1. {registration_data['country_preference_1']}
2. {registration_data['country_preference_2']}
3. {registration_data['country_preference_3']}

Experience: {registration_data['experience']}
Dietary Requirements: {registration_data['dietary_requirements']}

Emergency Contact: {registration_data['emergency_contact']}
Emergency Phone: {registration_data['emergency_phone']}
"""
        
        mail.send(msg)
        
        # Trimite email de confirmare către delegat
        confirmation_msg = Message(
            'Registration Confirmation - TimișoaraMUN 2025',
            sender=app.config['MAIL_USERNAME'],
            recipients=[registration_data['email']]
        )
        
        confirmation_msg.body = f"""
Dear {registration_data['first_name']} {registration_data['last_name']},

Thank you for registering for TimișoaraMUN 2025!

We have received your registration and will review your application. You will receive further information about committee and country assignments soon.

Conference Details:
Date: November 21-23, 2025
Location: Timișoara, Romania

If you have any questions, please contact us at delegate.registration@timisoara-mun.ro

Best regards,
TimișoaraMUN Secretariat
"""
        
        mail.send(confirmation_msg)
        
    except Exception as e:
        print(f"Email sending failed: {str(e)}")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and users[username] == password:
            session['username'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/admin')
@login_required
def admin_dashboard():
    registrations = Registration.query.all()
    return render_template('admin/adminboard.html', registrations=registrations)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/menteneanta')
def menteneanta():
    return render_template('menteneanta.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html'), 500

# Pentru producție pe Hostico
def create_app():
    with app.app_context():
        db.create_all()
    return app

# Pentru rularea cu CGI pe Hostico
if __name__ == '__main__':
    # Dezvoltare locală
    with app.app_context():
        db.create_all()
    app.run(debug=False)
else:
    # Producție pe Hostico
    application = create_app()