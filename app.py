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

CONTACT_EMAIL = os.getenv('CONTACT_EMAIL', 'contact@timisoara-mun.ro')

users = {
    "dragos@timisoara-mun.ro": "dragosSecretariatMunIntern",
    "cristiana@timisoara-mun.ro": "cristianaSecretariatMunIntern",
    "erol@timisoara-mun.ro": "erolSecretariatMunIntern",
    "secretariat@timisoara-mun.ro": "secretariatSecretariatMunIntern",
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
app.config['MAIL_DEFAULT_SENDER'] = (
    os.environ.get('MAIL_DEFAULT_SENDER')
    or app.config.get('MAIL_USERNAME')
    or CONTACT_EMAIL
)


# Configurare baza de date pentru producție cu cale absolută
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'tm_mun.db')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', f"sqlite:///{db_path}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mail = Mail(app)
db.init_app(app)


def _parse_recipients(value, fallback):
    raw = value or fallback or ""
    return [email.strip() for email in raw.split(',') if email and email.strip()]

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

committees = {
    'crisis': {
        'name': 'CRISIS Committee',
        'abbreviation': 'CRISIS',
        'spots': 15,
        'difficulty': 'Intermediate',
        'image': 'img/COMITETE/CRISIS.webp',
        'description': (
            'The Crisis Committee immerses delegates in a fast-paced simulation where decisions reverberate '
            'immediately across cabinets, alliances, and the press. Participants represent key actors with '
            'distinct objectives, crafting directives and personal actions as scenarios evolve in real time. '
            'It rewards creativity, strategic thinking, and the ability to keep calm when the situation changes minute by minute.'
        )
    },
    'c24': {
        'name': 'The Special Committee on Decolonization (C-24)',
        'abbreviation': 'C-24',
        'spots': 25,
        'difficulty': 'Intermediate',
        'image': 'img/COMITETE/The Special Committee on Decolonization (C-24).webp',
        'description': (
            'C-24 examines the unfinished agenda of decolonization and the lived realities of Non-Self-Governing Territories. '
            'Delegates evaluate self-determination claims, economic transitions, and the responsibilities of administering powers. '
            'Expect nuanced negotiations that balance historical justice with practical governance and regional stability.'
        )
    },
    'disec': {
        'name': 'Disarmament and International Security Committee (DISEC)',
        'abbreviation': 'DISEC',
        'spots': 25,
        'difficulty': 'Beginner',
        'image': 'img/COMITETE/Disarmament and International Security Committee.webp',
        'description': (
            'DISEC tackles questions of global peace and collective security, from conventional arms control to emerging cyber threats. '
            'Delegates build consensus-driven resolutions that reduce escalation risks while respecting national priorities. '
            'It is an ideal arena for new delegates to learn procedure while discussing timely security concerns.'
        )
    },
    'unodc': {
        'name': 'United Nations Office on Drugs and Crime (UNODC)',
        'abbreviation': 'UNODC',
        'spots': 25,
        'difficulty': 'Intermediate',
        'image': 'img/COMITETE/United Nations Office on Drugs and Crime.webp',
        'description': (
            'UNODC unites states in combating illicit trafficking, corruption, and transnational organized crime. '
            'Delegates weigh questions of law enforcement capacity, human rights safeguards, and international cooperation. '
            'Sessions focus on pragmatic frameworks that help states dismantle criminal networks while supporting vulnerable communities.'
        )
    },
    'unsc': {
        'name': 'United Nations Security Council (UNSC)',
        'abbreviation': 'UNSC',
        'spots': 15,
        'difficulty': 'Expert',
        'image': 'img/COMITETE/United Nations Security Council.webp',
        'description': (
            'The Security Council bears primary responsibility for maintaining international peace and security. '
            'Delegates navigate high-stakes crises, balance national interests, and manage the dynamics of the veto power. '
            'Success requires rapid negotiation, sharp diplomacy, and a firm grasp of international law and precedent.'
        )
    },
    'sochum': {
        'name': 'Social, Humanitarian and Cultural Committee (SOCHUM)',
        'abbreviation': 'SOCHUM',
        'spots': 30,
        'difficulty': 'Beginner',
        'image': 'img/COMITETE/Social, Humanitarian and Cultural Committee.webp',
        'description': (
            'SOCHUM addresses the human dimension of international affairs, from protecting minorities to supporting refugees and youth. '
            'Delegates craft people-centred responses that blend empathy with actionable policy. '
            'The committee welcomes first-time delegates ready to advocate for dignity, inclusion, and social justice.'
        )
    },
    'who': {
        'name': 'World Health Organization (WHO)',
        'abbreviation': 'WHO',
        'spots': 25,
        'difficulty': 'Intermediate',
        'image': 'img/COMITETE/World Health Organization.webp',
        'description': (
            'The WHO coordinates the global response to health emergencies and long-term public health challenges. '
            'Delegates debate equitable access to care, resilient health systems, and the ethics of international cooperation. '
            'Technical evidence meets humanitarian priorities as teams design responses that save lives.'
        )
    },
    'icj': {
        'name': 'International Court of Justice (ICJ)',
        'abbreviation': 'ICJ',
        'spots': 15,
        'difficulty': 'Beginner',
        'image': 'img/COMITETE/International Court of Justice.webp',
        'description': (
            'The ICJ places delegates on the bench as judges or advocates resolving disputes between states. '
            'Cases test research skills, legal reasoning, and the ability to build persuasive written and oral arguments. '
            'Participants collaborate to deliver balanced judgments rooted firmly in international law.'
        )
    },
    'ecofin': {
        'name': 'Economic and Financial Affairs Committee (ECOFIN)',
        'abbreviation': 'ECOFIN',
        'spots': 30,
        'difficulty': 'Beginner',
        'image': 'img/COMITETE/Economic and Financial Affairs Committee.webp',
        'description': (
            'ECOFIN examines the global economy through the lens of sustainable growth, trade, and financial stability. '
            'Delegates explore policies that tackle inequality while fostering innovation and resilience. '
            'It is a welcoming forum for delegates eager to pair economic analysis with creative diplomacy.'
        )
    },
    'unhrc': {
        'name': 'Human Rights Council (UNHRC)',
        'abbreviation': 'UNHRC',
        'spots': 25,
        'difficulty': 'Beginner',
        'image': 'img/COMITETE/Human Rights Council.webp',
        'description': (
            'The Human Rights Council evaluates urgent rights concerns, from freedom of expression to the protection of civilians in conflict. '
            'Delegates investigate country situations, elevate the voices of affected communities, and develop principled recommendations. '
            'The committee emphasises respectful debate, coalition building, and concrete action for universal rights.'
        )
    }
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


@app.route('/chairperson-registration')
def chairperson():
    """Mirror the chairperson registration endpoint used in templates."""
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

@app.route('/sponsors')
def sponsors():
    return render_template('sponsors.html')

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
    image_url = url_for('static', filename=committee_info['image'])
    return render_template(
        'comitete.html',
        comitet=committee_info['abbreviation'],
        comitet_name=committee_info['name'],
        textcomitet=committee_info['description'],
        poza=image_url,
        spots=committee_info['spots'],
        difficulty=committee_info['difficulty']
    )

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/policies')
def policies():
    return render_template('policies.html')

@app.route('/privacy-terms')
def privacy_terms():
    return render_template('privacy-terms.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip()
        subject = (request.form.get('subject') or '').strip()
        message = (request.form.get('message') or '').strip()

        if not name or not email or not message:
            flash('Please fill in your name, email, and message before submitting.', 'error')
            return redirect(url_for('contact'))

        recipients = _parse_recipients(
            os.environ.get('CONTACT_RECIPIENTS'),
            CONTACT_EMAIL
        )

        if CONTACT_EMAIL not in recipients:
            recipients.append(CONTACT_EMAIL)

        if not recipients:
            app.logger.error('Contact form submission failed: no recipients configured')
            flash('We could not deliver your message because no recipients are configured yet. Please try again later.', 'error')
            return redirect(url_for('contact'))

        subject_line = f"[Contact Form] {subject}" if subject else '[Contact Form] Message'
        sender = app.config.get('MAIL_DEFAULT_SENDER') or app.config.get('MAIL_USERNAME')

        try:
            msg = Message(subject_line, sender=sender, recipients=recipients)
            msg.body = (
                f"New contact form submission\n\n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Subject: {subject if subject else 'No subject provided'}\n\n"
                f"Message:\n{message}\n"
            )
            msg.reply_to = email
            mail.send(msg)
            flash('Your message has been sent! We will get back to you soon.', 'success')
        except Exception as exc:  # pragma: no cover - network dependent
            app.logger.exception('Failed to send contact form email: %s', exc)
            flash('Something went wrong while sending your message. Please try again later.', 'error')

        return redirect(url_for('contact'))

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


@app.route('/delegates')
def delegates_redirect():
    """Backward-compatible route forwarded to the delegates registration page."""
    return redirect(url_for('delegates_registration'))

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